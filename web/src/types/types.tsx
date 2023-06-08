export interface Counter {
    name:string;
    lat: number;
    lon: number;
    location_desc:string;
}

export interface Count{
    timestamp: Date;
    counter: string;
    mode:string;
    count_in: number;
    count_out:number;
}