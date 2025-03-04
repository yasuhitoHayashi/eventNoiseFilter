#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>

namespace py = pybind11;

struct Event {
    int x, y;  // 整数座標
    float time;

    Event(int x = 0, int y = 0, float time = 0) : x(x), y(y), time(time) {}
};

// 隣接ピクセルチェックのためのオフセット定義
const std::vector<std::pair<int, int>> NEIGHBOR_OFFSETS = {
    {0, 1}, {1, 0}, {0, -1}, {-1, 0},  // 上下左右
    {1, 1}, {-1, -1}, {1, -1}, {-1, 1} // 対角
};

// フィルタリング関数（隣接ピクセルベース）
std::vector<Event> filter_events(const std::vector<Event> &events, float tau, int K_threshold) {
    std::vector<Event> filtered_events;

    for (size_t i = 0; i < events.size(); ++i) {
        const Event &current = events[i];
        int valid_neighbors = 0;

        for (size_t j = 0; j < events.size(); ++j) {
            if (i == j) continue;
            const Event &neighbor = events[j];

            // 隣接ピクセル条件
            bool is_neighbor = false;
            for (const auto &offset : NEIGHBOR_OFFSETS) {
                if (neighbor.x == current.x + offset.first && neighbor.y == current.y + offset.second) {
                    is_neighbor = true;
                    break;
                }
            }

            if (is_neighbor) {
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
        .def(py::init<int, int, float>())
        .def_readwrite("x", &Event::x)
        .def_readwrite("y", &Event::y)
        .def_readwrite("time", &Event::time);

    m.def("filter_events", &filter_events, "Filter events based on spatial adjacency and temporal constraints",
          py::arg("events"), py::arg("tau"), py::arg("K_threshold"));
}