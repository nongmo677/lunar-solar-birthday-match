# -*- coding: utf-8 -*-
# 作者：nongmo677
# 功能说明：
#   这段脚本用来查找“哪些年份的同一天（公历）”在农历上也正好对应同一个月日。
#   举个例子：1995年12月6日的农历日期是几月几日？然后看看别的年份有没有这一天在农历上也是同样的月日。

from zhdate import ZhDate
from datetime import datetime

def get_lunar_from_gregorian(year, month, day):
    """
    输入一个公历日期，返回对应的农历月和日（只要月、日，不关心农历年份）。
    """
    greg_date = datetime(year, month, day)
    zh_date = ZhDate.from_datetime(greg_date)
    return zh_date.lunar_month, zh_date.lunar_day


def find_matching_years_by_gregorian_date(greg_year, greg_month, greg_day, start_year=1900, end_year=2100):
    """
    说明：
        给定一个公历日期，比如 1995-12-06，
        先求出这天对应的农历月日，
        然后在指定范围 [start_year, end_year] 内逐年检查，
        看哪些年份的农历“同月同日”刚好也是这一天的公历日期。
    """
    # 先拿到这天对应的农历月日
    lunar_month, lunar_day = get_lunar_from_gregorian(greg_year, greg_month, greg_day)
    
    print(f"参考公历 {greg_year}-{greg_month:02d}-{greg_day:02d} 的农历是：{lunar_month}月{lunar_day}日")

    results = []
    for y in range(start_year, end_year + 1):
        try:
            # 尝试构造这个年份的同农历月日
            zh_date = ZhDate(y, lunar_month, lunar_day)
            greg_date = zh_date.to_datetime()

            # 检查是否刚好对应公历的同一天
            if (greg_date.year == y and 
                greg_date.month == greg_month and 
                greg_date.day == greg_day):
                results.append((y, zh_date, greg_date))
        except ValueError:
            # 某些年份可能不存在这个农历日期（比如闰月或者日期越界）
            continue

    return results


# ===== 示例运行 =====
matches = find_matching_years_by_gregorian_date(
    greg_year=1995,
    greg_month=12,
    greg_day=6,
)

# 输出结果
if matches:
    print("\n符合条件的年份：")
    for year, zh, greg in matches:
        print(f"公历{greg.strftime('%Y年%m月%d日')} → 农历{year}年{zh.lunar_month}月{zh.lunar_day}日")
else:
    print("\n在给定范围内没有找到符合条件的年份。")
