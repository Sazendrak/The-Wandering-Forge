class Formatter:
    @staticmethod
    def render(data: dict, lead_ping: str, item_name: str, args, assistants: list) -> str:
        lines = []
        lines.append("=== Start of Craft ===")

        # Header
        header = f"**{lead_ping}** would like to craft the following **{data['quantity']}x {item_name}**"
        if getattr(args, 'selfless', False) and getattr(args, 'recipient_ping', None):
            header += f" for **{args.recipient_ping}**"
        lines.append(header)
        lines.append("")

        # Assistants
        lines.append("**Assisting Crafters / Workers:**")
        if assistants:
            for ast in assistants:
                lines.append(ast)
        else:
            lines.append("None")
        lines.append("Will assist.")
        lines.append("")

        # Process Narrative
        process_narrative = f"Crafting {item_name} (Tier: {args.tier.capitalize()})."
        if getattr(args, 'reforge', False): process_narrative += " Reforging existing item."
        if getattr(args, 'silver', False): process_narrative += " Applying silvering."
        if getattr(args, 'consumable', False): process_narrative += " Item is a consumable."
        lines.append("**Process:**")
        lines.append(process_narrative)
        lines.append("")

        # Time Metrics
        lines.append("**Time Metrics (DT Used):**")
        if getattr(args, 's', False):
            lines.append(f"Formula: {data['time_formula']}")
        lines.append(f"Final Time: **{data['final_time_days']:.2f} days**")
        lines.append("")

        # Sacrifice
        if getattr(args, 'sacrifice', None):
            lines.append(f"**Sacrifice:** {args.sacrifice}")
            lines.append("")

        # Expense Breakdown
        lines.append("**Expense Breakdown:**")
        if getattr(args, 's', False):
            base_cost = data['total_items_cost'] - data['extras_gp_total']
            lines.append(f"Calculations: {base_cost:.2f}g + ({data['wage_rate']}g x {data['total_team_count']} workers x {data['final_time_days']:.2f}d) + {data['extras_gp_total']:.2f}g")

        lines.append(f"Total Expense: {data['calculated_overhead']:.2f}g + {data['total_tax']:.2f}g tax = **{data['total_expense']:.2f}g**")
        lines.append("")

        # Payout Allocation
        lines.append("**Payout Allocation:**")
        if getattr(args, 's', False):
            lines.append(f"Wages: {data['wage_rate']}g x {data['paid_workers']} paid workers x {data['final_time_days']:.2f}d = {data['total_paid_wages']:.2f}g")

        unpaid_str_list = []
        if data['unpaid_workers'] >= 1: unpaid_str_list.append("Lead")
        if data['unpaid_workers'] >= 2: unpaid_str_list.append("Sim")
        unpaid_str = " & ".join(unpaid_str_list) if unpaid_str_list else "None"

        lines.append(f"Payout: {data['total_paid_wages']:.2f}g / {data['paid_workers']} workers = **{data['payout_per_worker']:.2f}g each** - {unpaid_str} (Unpaid)")
        lines.append("")

        # Materials
        monster_part = f" ({args.monster_part})" if getattr(args, 'monster_part', None) else ""
        lines.append("**Materials (Mats):**")
        lines.append(f"{data['quantity']}x {data['material_rarity_and_cr']}{monster_part}")
        lines.append("=== End of Craft ===")

        return "\n".join(lines)
