import {gql} from "@apollo/client";
import {Renter} from "../types/calendar.ts";

export interface RenterQueryResponse {
  renter: Renter;
}

export const GQL_RENTER_QUERY = gql`
  query renter($renterId: Int!) {
    renter(renter_id: $renterId) {
      id
      name
    }
  }
`;

export interface RentersQueryResponse {
  renters: Renter[];
}

export const GQL_RENTERS_QUERY = gql`
  query renters {
    renters {
      id
      name
    }
  }
`;

export interface RentStat {
  renter: Renter;
  storage: number;
  shop: number;
  total: number;
  paid: number;
}

export interface RentStatsCalendarContent {
  date: Date;
  values: RentStat[];
}

export interface RentStatsResponse {
  rentStats: {
    visible_dates: Date[];
    calendar_contents: RentStatsCalendarContent[];
  };
}

export const GQL_RENT_STATS = gql`
  query rentStats {
    rentStats {
      visible_dates
      calendar_contents {
        date
        values {
          renter {
            id
            name
          }
          storage
          shop
          total
          paid
        }
      }
    }
  }
`;
