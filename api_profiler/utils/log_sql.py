from django.conf import settings
from django.db import connection


class LogColors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"


class SqlLogging:

    @staticmethod
    def format_sql_logs(raw_sql: str):
        SQL_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                    'ON', 'GROUP BY', 'ORDER BY', 'LIMIT', 'OFFSET', 'AND', 'OR', 'HAVING']
        sql = raw_sql.replace('"', '').replace(',', ', ')
        for keyword in SQL_KEYWORDS:
            sql = sql.replace(keyword, f"\n{LogColors.BOLD}{keyword}{LogColors.RESET}")
        return sql.strip()

    @staticmethod
    def log_sql_queries(request, limit_sql_queries):
        if (
            len(connection.queries) == 0
        ):
            return
        total_time = 0.0
        line_sep = "-" * 80
        msg_parts = [f"\n{LogColors.CYAN}{line_sep}{LogColors.RESET}"]

        # Header
        msg_parts.append(f"{LogColors.BOLD}{LogColors.MAGENTA}SQL Queries Summary{LogColors.RESET}")
        msg_parts.append(f"{LogColors.YELLOW}Path     : {request.path_info}{LogColors.RESET}")
        msg_parts.append(f"{LogColors.YELLOW}Total    : {len(connection.queries)} queries{LogColors.RESET}")

        for idx, query in enumerate(connection.queries, start=1):
            if idx > limit_sql_queries:
                break
            raw_sql = query.get("sql", "")
            time_taken = float(query.get("time", 0))
            total_time += time_taken

            if True:
                formatted_sql = SqlLogging.format_sql_logs(raw_sql)
                msg_parts.append(f"{LogColors.GREEN}[{idx:03}]{LogColors.RESET}")
                msg_parts.append(f"{formatted_sql}")
                msg_parts.append(f"{LogColors.CYAN}       Time: {time_taken:.3f} sec{LogColors.RESET}\n")

        msg_parts.append(f"{LogColors.YELLOW}Total Execution Time: {total_time:.3f} sec{LogColors.RESET}")
        msg_parts.append(f"{LogColors.CYAN}{line_sep}{LogColors.RESET}\n")

        return "\n".join(msg_parts)