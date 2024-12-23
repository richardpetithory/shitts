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
