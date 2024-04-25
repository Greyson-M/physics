#pragma once
#include <vector>
#include "SFML/Graphics.hpp"

class Grid
{
public:
	struct cell {
		const int cell_capacity = 4; //max number of objects in a cell
		int cell_x, cell_y, object_count; //cell coordinates and number of objects in the cell

		

		Mass* objects[4] = {}; //stores the objects

		
		cell() : cell_x(0), cell_y(0), object_count(0) {};
		cell(int x, int y);

		void printCell() const;
		void add_object(Mass* particle);
		void remove_object(int object_idx);
		void clear();

	};


	int grid_width, grid_height, cell_size;
	std::vector<std::vector<cell*>> cells;

	
	Grid(): grid_width(0), grid_height(0){};
	Grid(int width, int height);

	void initGrid();
	
	bool inBounds(int x, int y) const;
	sf::Vector2i getCellIndex(int x, int y) const;
	void printCells() const;
	void insert(Mass* particle);
	void clearGrid();
	void draw(sf::RenderWindow* window) const;


};

