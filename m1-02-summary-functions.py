def checking_keys(data, required_keys):
    return [i for i, record in enumerate(data) if not all(k in record for k in required_keys)]


def clean_data(raw_data):
    cleaned = []
    for record in raw_data:
        cat = str(record['category']).strip().capitalize()

        res = record['resolution_minutes']
        try:
            if res is None:
                continue
            res = int(res)
        except:
            continue

        new_record = record.copy()
        new_record['category'] = cat
        new_record['resolution_minutes'] = res
        cleaned.append(new_record)

    return cleaned

def avg_res_by_cat(data):
    cat_totals = {}
    cat_counts = {}

    for record in data:
        cat = record['category']
        res = record['resolution_minutes']
        cat_totals[cat] = cat_totals.get(cat, 0) + res
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    return {cat: round(cat_totals[cat] / cat_counts[cat], 2) for cat in cat_totals}

def tickets_per_customer(data):
    cust_counts = {}
    for record in data:
        cid = record['customer_id']
        cust_counts[cid] = cust_counts.get(cid, 0) + 1
    return cust_counts

def escalation_metrics(data):
    overall_esc = sum(1 for r in data if r['escalated'])
    overall_rate = overall_esc / len(data) if data else 0

    cat_esc = {}
    cat_total = {}
    for r in data:
        cat = r['category']
        cat_total[cat] = cat_total.get(cat, 0) + 1
        if r['escalated']:
            cat_esc[cat] = cat_esc.get(cat, 0) + 1

    cat_rates = {cat: round(cat_esc.get(cat, 0) / cat_total[cat], 4) for cat in cat_total}

    return {
        'overall_rate' : round(overall_rate, 4),
        'by_category' : cat_rates,
        "category_counts": cat_total
    }

def package_final_report(avg_res, cust_counts, esc_metrics, data_len):
    report = {
        "report_metadata": {
            "total_records_processed": data_len,
            "unique_customers": len(cust_counts)
        },
        "resolution_metrics": {
            "avg_time_by_category": avg_res
        },
        "escalation_metrics": {
            "overall_rate": esc_metrics['overall_rate'],
            "rate_by_category": esc_metrics['by_category']
        }
    }
    return report
