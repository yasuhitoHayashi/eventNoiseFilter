#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <deque>
#include <unordered_map>
#include <algorithm>
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

std::vector<Event> filter_events(const std::vector<Event> &events, float tau, int K_threshold) {
    if (events.empty()) {
        return {};
    }

    // 時間順にソートされたイベントを保持
    std::vector<Event> sorted_events = events;
    std::sort(sorted_events.begin(), sorted_events.end(), [](const Event &a, const Event &b) {
        return a.time < b.time;
    });

    std::vector<int> neighbor_count(sorted_events.size(), 0);

    // 座標をキーとした時間キューを保持し、一定時間以上経過したイベントは逐次削除する
    struct PairHash {
        std::size_t operator()(const std::pair<int, int> &p) const noexcept {
            return (static_cast<std::size_t>(p.first) << 32) ^ static_cast<std::size_t>(p.second);
        }
    };

    std::unordered_map<std::pair<int, int>, std::deque<std::size_t>, PairHash> index_map;

    std::size_t start = 0;
    for (std::size_t i = 0; i < sorted_events.size(); ++i) {
        const Event &current = sorted_events[i];

        // 有効時間ウィンドウ外のイベントを削除
        while (sorted_events[i].time - sorted_events[start].time > tau) {
            auto key = std::make_pair(sorted_events[start].x, sorted_events[start].y);
            auto it = index_map.find(key);
            if (it != index_map.end() && !it->second.empty()) {
                it->second.pop_front();
                if (it->second.empty()) {
                    index_map.erase(it);
                }
            }
            ++start;
        }

        int count = 0;
        // 近傍ピクセルに存在するイベントの数を集計
        for (const auto &offset : NEIGHBOR_OFFSETS) {
            auto key = std::make_pair(current.x + offset.first, current.y + offset.second);
            auto it = index_map.find(key);
            if (it != index_map.end()) {
                count += static_cast<int>(it->second.size());
                // 近傍イベントにもカウントを加算
                for (std::size_t idx : it->second) {
                    neighbor_count[idx]++;
                }
            }
            if (count >= K_threshold) {
                break;
            }
        }

        neighbor_count[i] += count;

        // 現在のイベントをインデックスに追加
        index_map[std::make_pair(current.x, current.y)].push_back(i);
    }

    std::vector<Event> filtered_events;
    filtered_events.reserve(sorted_events.size());

    for (std::size_t i = 0; i < sorted_events.size(); ++i) {
        if (neighbor_count[i] >= K_threshold) {
            filtered_events.push_back(sorted_events[i]);
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