export interface Renter {
  id: number;
  name: string;
}

export interface RentStat {
  renter: Renter;
  storage: number;
  shop: number;
  access: boolean;
  bikes: number;
  paid: number;
}

export interface RentStatsCalendarContent {
  date: Date;
  rent: number;
  values: RentStat[];
}
