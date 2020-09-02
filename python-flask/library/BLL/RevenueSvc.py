from library.DAL import RevenueRep


def Revenue():
    count = 0
    today_total = 0
    prev_total = 0
    total = 0
    order_count = RevenueRep.OrderCountToday()
    revenue_today = RevenueRep.RevenueToday()
    percentage_with_prev_day = RevenueRep.PercentageWithPrevDay()
    revenue_total = RevenueRep.TotalRevenue()

    for order_count_today in order_count:
        if order_count_today:
            count += 1
        else:
            count = count

    for today_price in revenue_today:
        if revenue_today:
            today_total += today_price.total
        else:
            today_total = today_total

    for prev_price in percentage_with_prev_day:
        if prev_price:
            prev_total += prev_price.total
        else:
            prev_total = prev_total

    for total_price in revenue_total:
        if total_price:
            total += total_price.total
        else:
            total = total
    percentage = ((today_total - prev_total) / total) * 100
    result_order_count = {
        "labels": "Tổng sô đơn hang trong ngay",
        "order_count": count
    }
    result_today_total = {
        "labels": "Tổng sô doanh thu trong ngay",
        "order_count": today_total
    }
    result_percentage = {
        "labels": "So với hôm qua",
        "order_count": round(percentage, 2)
    }
    return result_order_count,result_today_total, result_percentage
