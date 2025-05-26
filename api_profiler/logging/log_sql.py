from collections import defaultdict
from django.conf import settings
from django.db import connection

from api_profiler.cache import cache


class LogColors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RED= "\033[91m"


class SqlLogging:

    @staticmethod
    def format_sql_logs(raw_sql: str)-> str:
        SQL_KEYWORDS = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                    'ON', 'GROUP BY', 'ORDER BY', 'LIMIT', 'OFFSET', 'AND', 'OR', 'HAVING']
        sql = raw_sql.replace('"', '').replace(',', ', ')
        for keyword in SQL_KEYWORDS:
            sql = sql.replace(keyword, f"\n{LogColors.BOLD}{keyword}{LogColors.RESET}")
        return sql.strip()

    @staticmethod
    def log_sql_queries(request, limit_sql_queries)->str:
        """
        Format and return a summary of SQL queries for the current request.

        Args:
            request: The Django request object.
            limit_sql_queries: The maximum number of queries to display.

        Returns:
            A formatted string summarizing the SQL queries, or None if no queries were executed.
        """
        if not connection.queries:
            return

        total_time = 0.0
        line_sep = "-" * 80
        msg_parts = [f"\n{LogColors.CYAN}{line_sep}{LogColors.RESET}"]

        # Header
        msg_parts.append(f"{LogColors.BOLD}{LogColors.MAGENTA}SQL Queries Summary{LogColors.RESET}")
        msg_parts.append(f"{LogColors.YELLOW}Path     : {request.path_info}{LogColors.RESET}")
        msg_parts.append(f"{LogColors.YELLOW}Total    : {len(connection.queries)} queries{LogColors.RESET}")

        # Grouping queries
        query_map = defaultdict(list)
        for q in connection.queries:
            sql = q.get("sql", "").strip()
            query_map[sql].append(float(q.get("time", 0)))

        # Sorting by repetition count desc, then total time desc
        sorted_queries = sorted(
            query_map.items(),
            key=lambda item: (-len(item[1]), -sum(item[1]))
        )

        # Display queries
        for idx, (sql, times) in enumerate(sorted_queries, start=1):
            if idx > limit_sql_queries:
                break

            count = len(times)
            total_query_time = sum(times)
            total_time += total_query_time

            # Flag long queries
            warning_msg = ""
            if total_query_time * 1000 > int(cache.get_int("SQL_TIME_THRESHOLD_IN_MS", 1000)):
                warning_msg = f"{LogColors.YELLOW}{LogColors.BOLD} ⚠️  "

            formatted_sql = SqlLogging.format_sql_logs(sql)

            msg_parts.append(f"{LogColors.GREEN}[{idx:03}]{LogColors.RESET}")
            msg_parts.append(f"{formatted_sql}")
            msg_parts.append(
                f"{LogColors.CYAN}       Repeated: {count}x | {warning_msg}Total Time: {total_query_time:.3f} sec{LogColors.RESET}\n"
            )

        msg_parts.append(f"{LogColors.YELLOW}Total Execution Time: {total_time:.3f} sec{LogColors.RESET}")
        msg_parts.append(f"{LogColors.CYAN}{line_sep}{LogColors.RESET}\n")

        return "\n".join(msg_parts)