import calendar
from datetime import datetime
import argparse
import sys


class DateGenerator:
    def __init__(self, year_input, level):
        self.year_input = year_input
        self.level = level
        self.year_list = []
        self.date_list = []
        
        self.initialize()
        self.generate_date_variants()

    def initialize(self):
        """解析年份输入并初始化年份列表"""
        if self.year_input:
            if "-" in self.year_input and "," in self.year_input:
                sys.exit("指定年份时短横杆和逗号不能同时使用")

            elif "-" not in self.year_input and "," not in self.year_input:
                try:
                    self.year_list.append(int(self.year_input))
                except Exception as e:
                    sys.exit(e)

            else:
                if "," in self.year_input:
                    years = self.year_input.split(",")
                    for year in years:
                        try:
                            self.year_list.append(int(year))
                        except Exception as e:
                            sys.exit(e)
                else:
                    year_range = self.year_input.split("-")
                    for year in range(int(year_range[0]), int(year_range[1]) + 1):
                        self.year_list.append(year)
        else:
            current_year = datetime.now().year
            self.year_list.append(current_year)

        self.year_list = sorted(self.year_list)

    def generate_date_variants(self):
        """生成日期变体"""
        for year in self.year_list:
            y2 = str(year)[2:]  # 两位年份
            y4 = str(year)  # 四位年份

            for month in range(1, 13):
                m = f"{month:02}"  # 两位月份
                m1 = str(month)  # 一位月份（不带前导零）

                # 获取每月的实际天数
                _, days_in_month = calendar.monthrange(year, month)

                for day in range(1, days_in_month + 1):
                    d = f"{day:02}"  # 两位日期
                    d1 = str(day)  # 一位日期（不带前导零）

                    # 基础日期格式
                    base_formats = [
                        f"{y4}{m}",  # 202501
                        f"{y4}-{m}",  # 2025-01
                        f"{y4}_{m}",  # 2025_01
                        f"{y2}{m}",  # 2501
                        f"{y2}-{m}",  # 25-01
                        f"{y2}_{m}",  # 25_01
                        f"{y4}{m}{d}",  # 20250101
                        f"{y4}-{m}-{d}",  # 2025-01-01
                        f"{y4}_{m}_{d}",  # 2025_01_01
                        f"{y2}{m}{d}",  # 250101
                        f"{y2}-{m}-{d}",  # 25-01-01
                        f"{y2}_{m}_{d}",  # 25_01_01
                        f"{y4}-{m1}-{d1}",  # 2025-1-1
                        f"{y4}_{m1}_{d1}",  # 2025_1_1
                    ]

                    self.date_list.extend(base_formats)

                    if self.level >= 2:
                        level2_formats = [
                            f"{m}{y4}",  # 012025
                            f"{m}-{y4}",  # 01-2025
                            f"{m}_{y4}",  # 01_2025
                            f"{m}-{y2}",  # 01-25
                            f"{m}_{y2}",  # 01_25
                            f"{d}{m}{y4}",  # 01012025
                            f"{d}_{m}_{y2}",  # 01_01_25
                            f"{d}-{m}-{y2}",  # 01-01-25
                            f"{d}_{m}_{y4}",  # 01_01_2025
                            f"{d}-{m}-{y4}",  # 01-01-2025
                            f"{m}{y2}",  # 0125
                            f"{d}{m}{y2}",  # 010125
                            f"{m1}{d1}{y4}",  # 1112025
                            f"{m1}-{d1}-{y4}",  # 1-1-2025
                            f"{m1}_{d1}_{y4}",  # 1_1_2025
                        ]
                        self.date_list.extend(level2_formats)

                    if self.level >= 3:
                        level3_formats = [
                            f"{m}{d}{y4}",  # 01012025 (美式)
                            f"{m}-{d}-{y4}",  # 01-01-2025 (美式)
                            f"{m}_{d}_{y4}",  # 01_01_2025 (美式)
                            f"{m}{d}{y2}",  # 010125 (美式)
                            f"{m}-{d}-{y2}",  # 01-01-25 (美式)
                            f"{m}_{d}_{y2}",  # 01_01_25 (美式)
                        ]
                        self.date_list.extend(level3_formats)

        # 去重
        self.date_list = list(set(self.date_list))

    def get_date_list(self):
        """返回生成的日期列表"""
        return self.date_list


def main():
    parser = argparse.ArgumentParser(description='日期生成工具')
    parser.add_argument("-y", "--year", help="指定年份范围,例如: -y 2022,2023,2024,2025 或 -y 2022-2025",
                        required=False)
    parser.add_argument('-level', '--level', dest="level", required=False, help='指定级别,级别越高生成的数量越多,一共3个级别',
                        default=1, type=int)
    parser.add_argument('-o', '--output', dest="output_filename", required=False, help='将结果输出到指定文件')
    
    # 检查是否有参数传入
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()

    # 创建日期生成器实例
    date_gen = DateGenerator(args.year, args.level)
    date_list = date_gen.get_date_list()

    # 处理输出
    if args.output_filename:
        with open(args.output_filename, 'w') as f:
            for date_fmt in date_list:
                f.write(date_fmt + '\n')
        print(f"已生成 {len(date_list)} 个日期格式并保存到 {args.output_filename}")
    else:
        for date_fmt in date_list:
            print(date_fmt)


if __name__ == '__main__':
    main()
