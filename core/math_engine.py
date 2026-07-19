from config.craft_config import Config
import re

class MathEngine:
    @staticmethod
    def get_tax_rate(cost: float) -> float:
        if cost < Config.TAX_THRESHOLD_GP:
            return 0.0
        for threshold, rate in Config.TAX_BRACKETS:
            if cost >= threshold:
                return rate
        return 0.0

    @classmethod
    def calculate(cls, tier: str, value: float = 0.0, quantity: int = 1,
                  reforge: bool = False, silver: bool = False, barding_size: str = None,
                  consumable: bool = False, sacrifice_tier: str = None,
                  mia: bool = False, ms: bool = False, sims: int = 0,
                  assistants_count: int = 0, wage_rate: float = Config.DEFAULT_WAGE_RATE,
                  unpaid_workers_count: int = 1, notax: bool = False):

        tier_lower = str(tier).lower()
        is_scroll = "scroll" in tier_lower
        scroll_lvl = 0

        if is_scroll:
            match = re.search(r'\d+', tier_lower)
            scroll_lvl = int(match.group()) if match else 0
            if scroll_lvl not in Config.SCROLLS:
                raise ValueError(f"Scroll level {scroll_lvl} not found in configuration.")
            base_time = Config.SCROLLS[scroll_lvl]["time"]
            base_cost = Config.SCROLLS[scroll_lvl]["cost"]
        else:
            if tier_lower not in Config.TIERS:
                raise ValueError(f"Crafting tier '{tier}' not recognized.")
            if tier_lower == "mundane":
                base_time = Config.TIERS["mundane"]["time_formula"](value)
                base_cost = Config.TIERS["mundane"]["cost_formula"](value)
            else:
                base_time = Config.TIERS[tier_lower]["time"]
                base_cost = Config.TIERS[tier_lower]["cost"]

        run_time, run_cost, extras_gp = base_time, base_cost, 0.0
        time_steps = [f"{base_time:.2f}"]
        cost_steps = [f"{base_cost:.2f}"]

        # 1. Augmentations
        if reforge:
            run_time *= 0.5
            run_cost *= 0.5
            time_steps.append("* 0.5 (Reforge)")
            cost_steps.append("* 0.5 (Reforge)")

        if silver:
            if tier_lower == "mundane":
                new_val = value + 100.0
                run_time = Config.TIERS["mundane"]["time_formula"](new_val)
                run_cost = Config.TIERS["mundane"]["cost_formula"](new_val)
                time_steps = [f"{run_time:.2f} (Silvered Recalc)"]
                cost_steps = [f"{run_cost:.2f} (Silvered Recalc)"]
            else:
                silver_days = 3.0 / Config.WORKDAY_HOURS
                run_time += silver_days
                extras_gp += 100.0
                time_steps.append(f"+ {silver_days:.3f} (Silvering)")
                cost_steps.append("+ 100.00 (Silvering)")

        if barding_size and barding_size.lower() in Config.BARDING_MODIFIERS:
            mod = Config.BARDING_MODIFIERS[barding_size.lower()]
            run_cost *= mod
            cost_steps.append(f"* {mod:.1f} (Barding)")

        # 2. Consumables
        if consumable:
            run_time *= 0.5
            run_cost *= 0.5
            time_steps.append("* 0.5 (Consumable)")
            cost_steps.append("* 0.5 (Consumable)")

        # 3. Sacrifice
        if sacrifice_tier and sacrifice_tier.lower() in Config.SACRIFICE_BASE_TIMES:
            reduction = Config.SACRIFICE_BASE_TIMES[sacrifice_tier.lower()] * 0.5
            run_time = max(Config.MIN_CRAFTING_DAYS, run_time - reduction)
            time_steps.append(f"- {reduction:.1f} (Sacrifice)")

        # 4. Class Features
        if mia and (tier_lower in ["common", "uncommon"] or (is_scroll and scroll_lvl <= 3)):
            run_time *= 0.25
            run_cost *= 0.5
            time_steps.append("* 0.25 (MIA)")
            cost_steps.append("* 0.5 (MIA)")

        if ms and is_scroll:
            run_time *= 0.5
            run_cost *= 0.5
            time_steps.append("* 0.5 (MS)")
            cost_steps.append("* 0.5 (MS)")

        # 5. Workers
        total_team = 1 + sims + assistants_count
        team_divisor = min(Config.MAX_TEAM_SIZE, total_team)
        final_time_days = run_time / team_divisor
        time_steps.append(f"/ {team_divisor} workers")

        # Payout & Tax
        paid_workers = max(0, total_team - unpaid_workers_count)
        total_paid_wages = paid_workers * wage_rate * final_time_days
        payout_per_worker = total_paid_wages / paid_workers if paid_workers > 0 else 0.0

        single_item_base_cost = run_cost + (extras_gp if not is_scroll else 0.0)
        if single_item_base_cost < Config.TAX_THRESHOLD_GP or notax:
            single_item_tax = 0.0
        else:
            single_item_tax = single_item_base_cost * cls.get_tax_rate(single_item_base_cost)

        total_tax = single_item_tax * quantity
        total_items_cost = single_item_base_cost * quantity
        calculated_overhead = total_items_cost + total_paid_wages

        mat_key = "common" if is_scroll and scroll_lvl <= 1 else \
                  "uncommon" if is_scroll and scroll_lvl <= 3 else \
                  "rare" if is_scroll and scroll_lvl <= 5 else \
                  "very rare" if is_scroll and scroll_lvl <= 8 else \
                  "legendary" if is_scroll else tier_lower

        return {
            "final_time_days": final_time_days, "total_team_count": total_team,
            "paid_workers": paid_workers, "total_paid_wages": total_paid_wages,
            "payout_per_worker": payout_per_worker, "single_item_cost": single_item_base_cost,
            "total_items_cost": total_items_cost, "total_tax": total_tax,
            "calculated_overhead": calculated_overhead, "total_expense": calculated_overhead + total_tax,
            "time_formula": " ".join(time_steps), "cost_formula": " ".join(cost_steps),
            "material_rarity_and_cr": Config.MATERIALS_MAP.get(mat_key, Config.MATERIALS_MAP["common"]),
            "extras_gp_total": extras_gp * quantity, "wage_rate": wage_rate, "quantity": quantity,
            "unpaid_workers": unpaid_workers_count
        }
