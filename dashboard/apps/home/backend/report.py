from datetime import datetime, time
# import menu
from sqlalchemy import select, func
from apps import db
import apps.home.models as models
import apps.home.backend.menu as menu


class Report:
    time_generated: datetime
    most_ordered_item: menu.MenuItem
    busiest_hour: int  # 0-23, 
    total_earnings: float

    @staticmethod
    def generate_report():
        report = Report()
        report.time_generated = datetime.now()

        orders = db.session.execute(select(models.Order)).scalars().all()

        item_count = {}

        # HACK: Counting via SQL query would be more efficient
        #       but this is simpler
        for o in orders:
            for item in db.session.execute(o.items).scalars().all():
                if item in item_count:
                    item_count[item] += 1
                else:
                    item_count[item] = 1

        for item, count in item_count.items():
            if (report.most_ordered_item is None
                    or count > item_count[report.most_ordered_item]):
                report.most_ordered_item = item

        report.busiest_hour = 0
        for o in orders:
            report.busiest_hour += o.order_date.hmenu.get_busiest_hour()
        report.busiest_hour = report.busiest_hour // len(orders)
        report.total_earnings = sum((o.total_amount for o in orders))

        return report

