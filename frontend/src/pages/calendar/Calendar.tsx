import {GQL_RENT_STATS, RentStatsResponse} from "@/lib/queries/calendar";
import {useQuery} from "@apollo/client";
import groupBy from "lodash/groupBy";

export const CalendarPage = () => {
  const {data} = useQuery<RentStatsResponse>(GQL_RENT_STATS, {
    variables: {},
  });

  if (!data) return null;

  const contentsByDate = groupBy(data.rentStats.calendar_contents, (rentStat) => rentStat.date.toString());

  console.log(contentsByDate);

  return (
    <div>
      {data.rentStats.visible_dates.map((date) => {
        console.log(contentsByDate[date.toString()]);

        return <div key={date.toString()}>{date.toString()}</div>;
      })}
    </div>
  );
};
