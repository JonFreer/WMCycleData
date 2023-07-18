export interface Counter {
  identity: number;
  name: string;
  lat: number;
  lon: number;
  location_desc: string;
}

export interface CounterPlus {
  identity: number;
  name: string;
  lat: number;
  lon: number;
  location_desc: string;
  today_count: number;
  this_week_count: number;
  yesterday_count: number;
  last_week_count: number;
}

export interface Count {
  timestamp: Date;
  counter: number;
  mode: string;
  count_in: number;
  count_out: number;
}
