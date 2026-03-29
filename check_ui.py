"""
Playwright audit script for Phase 15 checkpoint verification.
Checks all 7 items from the checklist.
"""
import time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8055"
RESULTS = []

def log(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    RESULTS.append((status, name, detail))
    marker = "OK" if passed else "!!"
    print(f"  [{marker}] {name}" + (f" -- {detail}" if detail else ""))


def navigate_to_system(page, system="mechanical"):
    """Click an 'Explore' button on the landing page to open a system view."""
    page.goto(BASE, wait_until="networkidle")
    time.sleep(2)

    # Try clicking the Explore button for the given system
    # The button has id={"type": "system-card-btn", "index": system}
    btn = page.locator(f'button[id*=\'"index": "{system}"\'], button[id*="index-{system}"]')
    # Dash pattern-matched IDs are serialized as JSON strings in the DOM
    # Use a more reliable selector: find any button near the system card title
    explore_btns = page.locator("button:has-text('Explore')")
    count = explore_btns.count()
    print(f"  Found {count} 'Explore' buttons on landing page")

    if count == 0:
        # Maybe we're already on a system view — check for System Comparison
        if page.locator("h4:has-text('System Comparison')").count() > 0:
            print("  Already on system view")
            return True
        print("  No Explore buttons found")
        return False

    # Click first Explore button (Mechanical)
    explore_btns.first.click()
    time.sleep(3)
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    section = page.locator("h4:has-text('System Comparison')")
    if section.count() > 0:
        section.scroll_into_view_if_needed()
        time.sleep(1)
        print("  Navigated to system view, scrolled to System Comparison")
        return True
    else:
        print("  System Comparison heading still not found after navigation")
        # Print page title and some content for debugging
        print(f"  Page title: {page.title()}")
        print(f"  Page URL: {page.url}")
        return False


def drag_slider(page, slider_id):
    slider = page.locator(f"#{slider_id}")
    if slider.count() == 0:
        return False
    box = slider.bounding_box()
    if not box:
        return False
    # Move from 20% to 80% of slider width
    start_x = box["x"] + box["width"] * 0.2
    end_x = box["x"] + box["width"] * 0.8
    mid_y = box["y"] + box["height"] / 2
    page.mouse.move(start_x, mid_y)
    page.mouse.down()
    page.mouse.move(end_x, mid_y, steps=10)
    page.mouse.up()
    time.sleep(2)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    return True


def get_label(page, label_id):
    el = page.locator(f"#{label_id}")
    if el.count() == 0:
        return None
    return el.inner_text()


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        print("\n=== Step 1: Navigate to system view ===")
        ok = navigate_to_system(page, "mechanical")
        if not ok:
            print("  FATAL: Could not navigate to system view. Dumping page HTML snippet...")
            html = page.content()
            print(html[:3000])
            browser.close()
            return [("FAIL", "Navigation", "Could not reach System Comparison section")]

        # ── Check 1: Chart IDs present ────────────────────────────────────────
        print("\n=== Check 1: Chart count (no old IDs) ===")
        chart_ids_found = []
        for cid in ["chart-cost", "chart-power", "chart-land", "chart-turbine", "chart-pie"]:
            if page.locator(f"#{cid}").count() > 0:
                chart_ids_found.append(cid)
        print(f"  Chart IDs in DOM: {chart_ids_found}")

        old_ids = [c for c in chart_ids_found if c in ("chart-land", "chart-turbine", "chart-pie")]
        has_cost = "chart-cost" in chart_ids_found
        has_power = "chart-power" in chart_ids_found

        log("chart-cost present", has_cost)
        log("chart-power present", has_power)
        log("No old chart-land/turbine/pie in DOM", not old_ids,
            f"old IDs still present: {old_ids}" if old_ids else "")

        # ── Check 2: Power breakdown bar traces ───────────────────────────────
        print("\n=== Check 2: Power breakdown chart content ===")
        power_chart = page.locator("#chart-power")
        if power_chart.count() > 0:
            power_text = power_chart.inner_text()
            has_groundwater = "Groundwater" in power_text
            has_ro = "RO Desalination" in power_text or "RO" in power_text
            has_brine = "Brine" in power_text
            print(f"  Power chart text snippet: {power_text[:200]!r}")
            log("Power chart contains 'Groundwater'", has_groundwater)
            log("Power chart contains 'RO'", has_ro)
            log("Power chart contains 'Brine'", has_brine)
        else:
            log("Power chart accessible", False, "chart-power not found after nav")

        # ── Check 3: Time Horizon slider ──────────────────────────────────────
        print("\n=== Check 3: Time Horizon slider ===")
        label_before = get_label(page, "label-years")
        print(f"  label-years before drag: {label_before!r}")
        dragged = drag_slider(page, "slider-time-horizon")
        if not dragged:
            log("Time Horizon slider exists", False, "slider-time-horizon not found")
        else:
            label_after = get_label(page, "label-years")
            print(f"  label-years after drag:  {label_after!r}")
            log("Time Horizon slider updates label-years", label_before != label_after,
                f"{label_before!r} -> {label_after!r}")

        # ── Check 4: Battery/Tank slider ──────────────────────────────────────
        print("\n=== Check 4: Battery/Tank slider ===")
        label_before = get_label(page, "label-battery-ratio")
        print(f"  label-battery-ratio before drag: {label_before!r}")
        dragged = drag_slider(page, "slider-battery")
        if not dragged:
            log("Battery/Tank slider exists", False, "slider-battery not found")
        else:
            label_after = get_label(page, "label-battery-ratio")
            print(f"  label-battery-ratio after drag:  {label_after!r}")
            log("Battery/Tank slider updates label-battery-ratio", label_before != label_after,
                f"{label_before!r} -> {label_after!r}")

        # ── Check 5: TDS slider ───────────────────────────────────────────────
        print("\n=== Check 5: TDS slider ===")
        label_before = get_label(page, "label-tds")
        print(f"  label-tds before drag: {label_before!r}")
        dragged = drag_slider(page, "slider-tds")
        if not dragged:
            log("TDS slider exists", False, "slider-tds not found")
        else:
            label_after = get_label(page, "label-tds")
            print(f"  label-tds after drag:  {label_after!r}")
            log("TDS slider updates label-tds", label_before != label_after,
                f"{label_before!r} -> {label_after!r}")

        # ── Check 6: Depth slider ─────────────────────────────────────────────
        print("\n=== Check 6: Depth slider ===")
        label_before = get_label(page, "label-depth")
        print(f"  label-depth before drag: {label_before!r}")
        dragged = drag_slider(page, "slider-depth")
        if not dragged:
            log("Depth slider exists", False, "slider-depth not found")
        else:
            label_after = get_label(page, "label-depth")
            print(f"  label-depth after drag:  {label_after!r}")
            log("Depth slider updates label-depth", label_before != label_after,
                f"{label_before!r} -> {label_after!r}")

        # ── Check 7: System badge toggles ─────────────────────────────────────
        print("\n=== Check 7: System badge toggles ===")
        for badge_id in ["legend-btn-mechanical", "legend-btn-electrical", "legend-btn-hybrid"]:
            btn = page.locator(f"#{badge_id}")
            if btn.count() > 0:
                btn.click(); time.sleep(0.8)
                btn.click(); time.sleep(0.8)
                log(f"Badge {badge_id} clickable", True)
            else:
                log(f"Badge {badge_id} exists", False)

        browser.close()

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    passed = [r for r in RESULTS if r[0] == "PASS"]
    failed = [r for r in RESULTS if r[0] == "FAIL"]
    for r in RESULTS:
        detail = f"\n        detail: {r[2]}" if r[2] else ""
        print(f"  [{r[0]}] {r[1]}{detail}")
    print(f"\n  {len(passed)} passed / {len(failed)} failed")
    return failed


if __name__ == "__main__":
    failures = run()
    exit(1 if failures else 0)
