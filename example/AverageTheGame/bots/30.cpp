#include <iostream>
using namespace std;

int main() {
	string line;
	cin >> line;
	while (line != "end") {
		cout << "30\n";
		cout.flush();
		cin >> line;
	}
	return 0;
}