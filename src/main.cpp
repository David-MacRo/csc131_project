#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <regex>
#include <cstdlib>

using namespace std;

struct Record {
    string name;
    string source;
    string dob;
    string address;

    vector<string> companies;

    Record() = default;
};

struct Node {
    Record data;
    Node* prev = nullptr;
    Node* next = nullptr;
    explicit Node(const Record& r) : data(r) {}
};

Class DoublyLinkedList {
private:
    Node* head = nullptr;
    Node* tail = nullptr;
    size_t sz = 0;

public: 
    ~DoublyLinkedList () {clear(); }

    void push_back(const Record& r) {
        Node* n = new Node(r);
        if (!tail) {
            head = tail = n;
        } else {
            tail->next = n;
            n->prev = tail;
            tail = n;
        }
        ++sz;
    }
}