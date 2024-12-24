import {GQL_RENT_STATS, RentStatsResponse} from "@/lib/queries/calendar";
import {useQuery} from "@apollo/client";
import {sortBy, sum} from "lodash";
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
          const infoForDate = sortBy(contentsByDate[date.toString()][0].values, [
            function (o) {
              return o.renter.name;
            },
          ]);
          const totalPaid = sum(infoForDate.map((rentInfo) => rentInfo.paid));
          const shopRent = contentsByDate[date.toString()][0].rent;
          return (
            <tr key={date.toString()}>
              <td>{date.toString()}</td>
              <td key={date.toString()}>
                <ul className="mb-0">
                  {infoForDate.map((rentInfo) => {
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
                <div>
                  ${shopRent} - ${totalPaid} = ${shopRent - totalPaid}
                </div>
              </td>
            </tr>
          );
        })}
      </tbody>
    </Table>
  );
};
