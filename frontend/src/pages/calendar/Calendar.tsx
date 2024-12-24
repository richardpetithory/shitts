import {GQL_RENT_STATS, RentStatsResponse} from "@/lib/queries/calendar";
import {useQuery} from "@apollo/client";
import groupBy from "lodash/groupBy";
import range from "lodash/range";
import {Table} from "react-bootstrap";
import {FaMotorcycle, FaRegBuilding} from "react-icons/fa";

export const CalendarPage = () => {
  const {data} = useQuery<RentStatsResponse>(GQL_RENT_STATS, {
    variables: {},
  });

  if (!data) return null;

  const contentsByDate = groupBy(data.rentStats.calendar_contents, (rentStat) => rentStat.date.toString());

  console.log(contentsByDate);

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Date</th>
          <th>Rent Info</th>
        </tr>
      </thead>
      <tbody>
        {data.rentStats.visible_dates.map((date) => {
          const infoForDate = contentsByDate[date.toString()][0];
          console.log(infoForDate);
          return (
            <tr key={date.toString()}>
              <td>{date.toString()}</td>
              <td key={date.toString()}>
                <ul className="mb-0">
                  {infoForDate.values.map((rentInfo) => {
                    const total = rentInfo.shop + rentInfo.storage;

                    const warningClass = rentInfo.paid < total ? "text-danger" : "";

                    return (
                      <li className={warningClass}>
                        <span className="p-1">
                          {rentInfo.renter.name} owed ${total} and paid ${rentInfo.paid}
                        </span>
                        for
                        <span className="p-1">{rentInfo.access && <FaRegBuilding />}</span>
                        <span className="p-1">
                          {range(rentInfo.bikes).map(() => (
                            <span className="pe-1">
                              <FaMotorcycle />
                            </span>
                          ))}
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </td>
            </tr>
          );
        })}
      </tbody>
    </Table>
  );
};
