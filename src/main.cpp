#include <iostream>
#include <string>
#include <vector>
// King Her was here.
//This is where the program starts
struct Record {
    string name;
    vector<string> companies;
    string source;

    Record() {}

    Record(string n, vector<string> c, string s)
        : name(n), companies(c), source(s) {}
};
