package com.sensor;

public class SensorReading {
    public String sensor_id;
    public double temperature;
    public double humidity;
    public double timestamp;

    public SensorReading() {} // Default constructor for Flink serialization

    @Override
    public String toString() {
        return "SensorReading{" +
                "id='" + sensor_id + '\'' +
                ", temp=" + temperature +
                ", hum=" + humidity +
                '}';
    }
}