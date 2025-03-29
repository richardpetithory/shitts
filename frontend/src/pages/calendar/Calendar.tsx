import {GQL_RENT_STATS, RentStatsResponse} from "@/lib/queries/calendar";
import {useQuery} from "@apollo/client";
import classNames from "classnames";
import {sortBy, sum} from "lodash";
import groupBy from "lodash/groupBy";
import {Table} from "react-bootstrap";
import {FaMotorcycle, FaRegBuilding} from "react-icons/fa";
import {Tooltip} from "react-tooltip";

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
                <ul className="mb-0 list-group">
                  {infoForDate.map((rentInfo) => {
                    const total = rentInfo.shop + rentInfo.storage;

                    const warningClass = rentInfo.paid < total ? "text-danger" : "";

                    return (
                      <li key={rentInfo.renter.id} className={classNames("list-group-item", warningClass)}>
                        <span className="p-1">
                          {rentInfo.renter.name} owed ${total} and paid ${rentInfo.paid}
                        </span>
                        for
                        <span className="p-1">
                          {rentInfo.access && (
                            <span>
                              <a id={"renter-" + rentInfo.renter.id.toString()}>
                                <FaRegBuilding />
                              </a>
                              <Tooltip anchorSelect={"#renter-" + rentInfo.renter.id.toString()} clickable>
                                Shop Rent
                              </Tooltip>
                            </span>
                          )}
                        </span>
                        <span className="p-1">
                          {rentInfo.bikes.map((bike) => (
                            <span key={bike.id} className="pe-1">
                              <a id={"bike-" + bike.id.toString()}>
                                <FaMotorcycle />
                              </a>
                              <Tooltip anchorSelect={"#bike-" + bike.id.toString()} clickable>
                                {bike.description}
                              </Tooltip>
                            </span>
                          ))}
                        </span>
                      </li>
                    );
                  })}
                  <li className="list-group-item">
                    <strong>
                      ${shopRent} - ${totalPaid} = ${shopRent - totalPaid}
                    </strong>
                  </li>
                </ul>
              </td>
            </tr>
          );
        })}
      </tbody>
    </Table>
  );
};
