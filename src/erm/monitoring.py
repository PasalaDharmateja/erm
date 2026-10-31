def apply_kri_flags(df, config):
    result = df.copy()
    warning = config["kri"]["overdue_days_warning"]
    critical = config["kri"]["overdue_days_critical"]
    def flag(days):
        if days >= critical:
            return "Critical"
        if days >= warning:
            return "Warning"
        return "Normal"
    result["overdue_kri_status"] = result["overdue_days"].apply(flag)
    return result
