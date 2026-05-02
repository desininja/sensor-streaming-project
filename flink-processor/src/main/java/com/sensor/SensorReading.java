package com.sensor;

public class SensorReading {
    public String sensor_id;
    public int distance_cm;
    public double timestamp;

    public SensorReading() {} // Default constructor for Flink serialization

    @Override
    public String toString() {
        return "Distance Alert: " + sensor_id + " is " + distance_cm + " cm away";
    }
}