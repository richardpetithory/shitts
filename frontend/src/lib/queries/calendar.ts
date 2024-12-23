import {gql} from "@apollo/client";
import {Renter} from "../types/calendar.ts";

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
