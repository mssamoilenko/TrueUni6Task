#include <string>

class Time {
private:
    int hours;
    int minutes;
    int seconds;

public:
    Time(int h = 0, int m = 0, int s = 0) : hours(h), minutes(m), seconds(s) {}

    void plusSecond() {
        seconds++;
        if (seconds >= 60) { seconds = 0; minutes++; }
        if (minutes >= 60) { minutes = 0; hours++; }
        if (hours >= 24) { hours = 0; }
    }

    std::string toString() const {
        return std::to_string(hours) + ":" +
               std::to_string(minutes) + ":" +
               std::to_string(seconds);
    }

    std::string to12HourString() const {
        int h = (hours == 0 || hours == 12) ? 12 : hours % 12;
        std::string period = (hours < 12) ? "AM" : "PM";
        return std::to_string(h) + ":" +
               std::to_string(minutes) + ":" +
               std::to_string(seconds) + " " + period;
    }
};

class Clock {
private:
    std::string manufacturer;
    bool is24HourFormat;
    Time time;

public:
    Clock(std::string brand, bool format, int h, int m, int s)
        : manufacturer(brand), is24HourFormat(format), time(h, m, s) {}

    void plusSecond() { time.plusSecond(); }

    std::string getInfo() const {
        return "Годинник: " + manufacturer + "\nЧас: " +
               (is24HourFormat ? time.toString() : time.to12HourString());
    }
};

// Функції для взаємодії з Python
extern "C" {
    Clock* createClock(const char* brand, bool format, int h, int m, int s) {
        return new Clock(brand, format, h, m, s);
    }
    void deleteClock(Clock* c) { delete c; }
    void clockPlusSecond(Clock* c) { c->plusSecond(); }
    const char* getClockInfo(Clock* c) {
        static std::string result;
        result = c->getInfo();
        return result.c_str();
    }
}
