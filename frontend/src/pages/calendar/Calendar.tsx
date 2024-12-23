import {GQL_RENTER_QUERY, RenterQueryResponse} from "@/lib/queries/calendar";
import {useQuery} from "@apollo/client";

export const CalendarPage = () => {
  const {data} = useQuery<RenterQueryResponse>(GQL_RENTER_QUERY, {
    variables: {
      renterId: 1,
    },
  });

  if (!data) return null;

  console.log(data);

  return (
    <div>
      {data.renter.name}
      {/*{data.renters.map((renter) => (*/}
      {/*  <div key={renter.id}>{renter.name}</div>*/}
      {/*))}*/}
    </div>
  );
};
