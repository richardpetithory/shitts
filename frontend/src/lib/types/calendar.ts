export interface Renter {
  id: number;
  name: string;
}

export interface Bike {
  id: number;
  description: string;
}

export interface RentStat {
  renter: Renter;
  storage: number;
  shop: number;
  access: boolean;
  bikes: Bike[];
  paid: number;
}

export interface RentStatsCalendarContent {
  date: Date;
  rent: number;
  values: RentStat[];
}
