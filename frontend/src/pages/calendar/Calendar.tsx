import {useQuery} from "@apollo/client";
import {GQL_RENTERS_QUERY, RentersQueryResponse} from "../../lib/queries/calendar.ts";

export const CalendarPage = () => {
  const {data} = useQuery<RentersQueryResponse>(GQL_RENTERS_QUERY, {
    variables: {},
  });

  if (!data) return null;

  return (
    <div>
      {data.renters.map((renter) => (
        <div key={renter.id}>{renter.name}</div>
      ))}
    </div>
  );
};
