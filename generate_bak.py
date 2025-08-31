import argparse
import calendar
import sys
from datetime import datetime
import tldextract


class BakFileNameGen:
    def __init__(self, domain, year, level, output_filename):
        self.domain = domain
        self.year = year
        self.year_list = []
        self.level = level
        self.output_filename = output_filename
        self.domain_variant_list = []
        self.date_list = []
        self.bak_suffix_list = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar', '.7z', '.bak', '.gz', '.tar.tgz',
                                '.backup']

        self.filename_list = [
            '0.rar', '0.zip', '1.bak', '1.rar', '1.zip', '2013.bak', '2016.bak', '2025.bak',
            '222.rar', '22.rar', '333.rar', '33.rar', 'abc.rar', 'admin.bak', 'admin.rar',
            'admin.zip', 'api.bak', 'api.rar', 'api.zip', 'archive.bak', 'asp.rar', 'asp.zip',
            'auth.bak', 'back.rar', '.backup', 'backup.bak', 'backupdata.rar', 'backup.rar',
            'backups.rar', 'backups.zip', 'backup.zip', 'back.zip', 'bak.bak', 'bak.rar',
            'bak.zip', 'bbs.bak', 'bbs.rar', 'bbs.zip', 'bin.bak', 'bin.rar', 'bin.zip',
            'blog.rar', 'clients.bak', 'code.bak', 'code.php.bak', 'com.rar', 'com.zip',
            'config.asp.bak', 'config_global.bak', 'config.php.bak', 'conf.php.bak',
            'conn.asp.bak', 'conn.php.bak', 'customers.bak', 'data.bak', 'database.bak',
            'database.rar', 'database.zip', 'data.rar', 'data.zip', 'dat.rar', 'dat.zip',
            'db.bak', 'db.rar', 'db.zip', 'files.bak', 'home.bak', 'html.bak', 'index.bak',
            'index.rar', 'index.zip', 'js.bak', 'jsp.rar', 'jsp.zip', 'js.rar', 'js.zip',
            'local.bak', 'log.bak', 'log.rar', 'log.zip', 'master.bak', 'my.rar', 'my.zip',
            'new.bak', 'new.rar', 'new.zip', 'old.bak', 'old.rar', 'old.zip', 'php.bak',
            'php.rar', 'php.zip', 'right.asp.bak', 'root.bak', 'root.rar',
            'root.zip', 'sample.zip', 'secring.bak', 'settings.php.bak', 'setup.aspx.bak',
            'setup.php.bak', 'sf.rar', 'shop.zip', 'site.bak', 'sitemetrics.zip', 'site.rar',
            'site.zip', 'sql1.rar', 'sql.bak', 'sql.rar', 'sql.zip', 's.rar',
            'tar.rar', 'tar.zip', 'temp.rar', 'temp.zip', 'test.bak', 'test.rar', 'test.zip',
            'uc_server.zip', 'user.rar', 'users.bak', 'users.tar', 'users.zip', 'vb.rar',
            'vb.zip', 'vivo.zip', 'wangzhan.zip', 'web.bak', 'web.config.bak', 'webmedia.rar',
            'web.rar', 'website.rar', 'website.zip', 'web.zip', 'wp.rar', 'wp.zip', 'www.bak',
            'www.rar', 'wwwroot.rar', 'wwwroot.zip', 'www.zip', '.zip'
        ]

    def initialize(self):
        if ":" in self.domain or "/" in self.domain:
            sys.exit("请提供标准的域名格式,例如: -d api.baidu.com")
        if self.year:
            if "-" in self.year and "," in self.year:
                sys.exit("指定年份时短横杆和逗号不能同时使用")

            elif "-" not in self.year and "," not in self.year:
                try:
                    self.year_list.append(int(self.year))
                except Exception as e:
                    sys.exit(e)

            else:
                if "," in self.year:
                    years = self.year.split(",")
                    for year in years:
                        try:
                            self.year_list.append(int(year))
                        except Exception as e:
                            sys.exit(e)
                else:
                    year_range = self.year.split("-")
                    for year in range(int(year_range[0]), int(year_range[1]) + 1):
                        self.year_list.append(year)
        else:
            self.year = datetime.now().year
            self.year_list.append(self.year)

        self.year_list = sorted(self.year_list)
        self.generate_date_variants()
        self.generate_domain_variants()

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

    def generate_domain_variants(self):
        # 分割域名部分
        parts = self.domain.split('.')
        # 添加原始域名
        self.domain_variant_list.append(self.domain)

        parsed_domain = tldextract.extract(self.domain)
        primary_domain = f"{parsed_domain.domain}.{parsed_domain.suffix}"
        self.domain_variant_list.append(primary_domain)
        self.domain_variant_list.append(primary_domain.split(".")[0])

        if self.level >= 2:
            # 生成连字符变体 (api.baidu.com -> api-baidu-com)
            type1 = '-'.join(parts)
            self.domain_variant_list.append(type1)

            # 生成下划线变体 (api.baidu.com -> api_baidu_com)
            type2 = '_'.join(parts)
            self.domain_variant_list.append(type2)

            type3 = ''.join(parts)
            self.domain_variant_list.append(type3)

    def generate_filename(self):
        # 域名+后缀
        for domain_variant in self.domain_variant_list:
            for suffix in self.bak_suffix_list:
                filename = domain_variant + suffix
                self.filename_list.append(filename)

        # 域名+日期+后缀
        for domain_variant in self.domain_variant_list:
            for date_fmt in self.date_list:
                for suffix in self.bak_suffix_list:
                    filename1 = domain_variant + '_' + date_fmt + suffix
                    filename2 = domain_variant + '-' + date_fmt + suffix
                    self.filename_list.append(filename1)
                    self.filename_list.append(filename2)
        # 日期+后缀
        for date_fmt in self.date_list:
            for suffix in self.bak_suffix_list:
                filename = date_fmt + suffix
                self.filename_list.append(filename)
        # 去重
        self.filename_list = list(set(self.filename_list))

    def process_result(self):
        if "-o" not in sys.argv and "--output" not in sys.argv:
            for filename in self.filename_list:
                print(filename)
        else:
            with open(self.output_filename, 'w') as f:
                for filename in self.filename_list:
                    f.write(filename + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', dest="domain", required=True, help='指定域名，例如: example.com')
    parser.add_argument("-y", "--year", help="指定年份范围,例如: -y 2022,2023,2024,2025 或 -y 2022-2025",
                        required=False)
    parser.add_argument('-level', '--level', dest="level", required=False, help='指定级别,级别越高生成的数量越多',
                        default=1, type=int)
    parser.add_argument('-o', '--output', dest="output_filename", required=False, help='将结果输出到指定文件')
    args = parser.parse_args()

    # 创建生成器实例
    bak_filename_gen = BakFileNameGen(args.domain, args.year, args.level, args.output_filename)
    bak_filename_gen.initialize()
    bak_filename_gen.generate_filename()
    bak_filename_gen.process_result()


if __name__ == '__main__':
    main()