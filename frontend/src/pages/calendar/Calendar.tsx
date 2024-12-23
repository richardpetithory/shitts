import {GQL_RENT_STATS, RentStatsResponse} from "@/lib/queries/calendar";
import {useQuery} from "@apollo/client";

export const CalendarPage = () => {
  const {data} = useQuery<RentStatsResponse>(GQL_RENT_STATS, {
    variables: {},
  });

  if (!data) return null;

  console.log(data);

  return (
    <div>
      dsf
      {/*{data.renters.map((renter) => (*/}
      {/*  <div key={renter.id}>{renter.name}</div>*/}
      {/*))}*/}
    </div>
  );
};
