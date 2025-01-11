#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>

namespace py = pybind11;

struct Event {
    float x, y, time;

    Event(float x = 0, float y = 0, float time = 0) : x(x), y(y), time(time) {}
};

// 2次元平面上の距離計算
inline float distance(const Event &a, const Event &b) {
    return std::sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}

// フィルタリング関数
std::vector<Event> filter_events(const std::vector<Event> &events, float N, float tau, int K_threshold) {
    std::vector<Event> filtered_events;

    for (size_t i = 0; i < events.size(); ++i) {
        const Event &current = events[i];
        int valid_neighbors = 0;

        for (size_t j = 0; j < events.size(); ++j) {
            if (i == j) continue;
            const Event &neighbor = events[j];

            // 空間的近傍の条件
            if (distance(current, neighbor) <= N) {
                // 時間的近傍の条件
                if (std::abs(current.time - neighbor.time) <= tau) {
                    valid_neighbors++;
                }
            }

            // 閾値を超えたらフィルタを通過
            if (valid_neighbors >= K_threshold) {
                filtered_events.push_back(current);
                break;
            }
        }
    }

    return filtered_events;
}

PYBIND11_MODULE(filter_events, m) {
    py::class_<Event>(m, "Event")
        .def(py::init<float, float, float>())
        .def_readwrite("x", &Event::x)
        .def_readwrite("y", &Event::y)
        .def_readwrite("time", &Event::time);

    m.def("filter_events", &filter_events, "Filter events based on spatial and temporal constraints",
          py::arg("events"), py::arg("N"), py::arg("tau"), py::arg("K_threshold"));
}