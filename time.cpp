#include <string>

// Клас "Час"
class Time {
private:
    int hours;   // Години
    int minutes; // Хвилини
    int seconds; // Секунди

public:
    // Конструктор з параметрами за замовчуванням
    Time(int h = 0, int m = 0, int s = 0) : hours(h), minutes(m), seconds(s) {}

    // Метод для додавання однієї секунди до часу
    void plusSecond() {
        seconds++;
        if (seconds >= 60) { seconds = 0; minutes++; } // Якщо секунди >= 60, обнулити та додати хвилину
        if (minutes >= 60) { minutes = 0; hours++; }   // Якщо хвилини >= 60, обнулити та додати годину
        if (hours >= 24) { hours = 0; }               // Якщо години >= 24, обнулити
    }

    // Метод для отримання часу у форматі 24-годин
    std::string toString() const {
        return std::to_string(hours) + ":" +
               std::to_string(minutes) + ":" +
               std::to_string(seconds);
    }

    // Метод для отримання часу у форматі 12-годин
    std::string to12HourString() const {
        int h = (hours == 0 || hours == 12) ? 12 : hours % 12; // Конвертація годин у 12-годинний формат
        std::string period = (hours < 12) ? "AM" : "PM";       // Визначення періоду (AM/PM)
        return std::to_string(h) + ":" +
               std::to_string(minutes) + ":" +
               std::to_string(seconds) + " " + period;
    }
};

// Клас "Годинник"
class Clock {
private:
    std::string manufacturer; // Назва виробника
    bool is24HourFormat;      // Формат часу (24-годинний чи 12-годинний)
    Time time;                // Об'єкт класу "Час"

public:
    // Конструктор для ініціалізації годинника
    Clock(std::string brand, bool format, int h, int m, int s)
        : manufacturer(brand), is24HourFormat(format), time(h, m, s) {}

    // Метод для додавання однієї секунди до часу годинника
    void plusSecond() { time.plusSecond(); }

    // Метод для отримання інформації про годинник
    std::string getInfo() const {
        return "Годинник: " + manufacturer + "\nЧас: " +
               (is24HourFormat ? time.toString() : time.to12HourString());
    }
};

// Функції для взаємодії з Python
extern "C" {
    // Створення об'єкта "Годинник"
    Clock* createClock(const char* brand, bool format, int h, int m, int s) {
        return new Clock(brand, format, h, m, s);
    }

    // Видалення об'єкта "Годинник"
    void deleteClock(Clock* c) { delete c; }

    // Додавання однієї секунди до часу годинника
    void clockPlusSecond(Clock* c) { c->plusSecond(); }

    // Отримання інформації про годинник у вигляді рядка
    const char* getClockInfo(Clock* c) {
        static std::string result;
        result = c->getInfo();
        return result.c_str();
    }
}
