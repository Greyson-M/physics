#include "Grid.h"
#include <iostream>


Grid::Grid(int width, int height)
{ 
	this->grid_width = width;
	this->grid_height = height;
	this->cell_size = 40;

	initGrid();

}

void Grid::initGrid()
{

	for (int i = 0; i < grid_width / cell_size; i++)
	{
		std::vector<cell*> row;
		for (int j = 0; j < grid_height / cell_size; j++)
		{
			cell* c = new cell(i, j);
			row.push_back(c);
		}
		cells.push_back(row);
	}
}

bool Grid::inBounds(int x, int y) const
{
	return x > 0 && x < grid_width && y > 1 && y < grid_height;
}

sf::Vector2i Grid::getCellIndex(int x, int y) const
{
	if (inBounds(x, y))
	{
		return sf::Vector2i((int)(x / cell_size), (int)(y / cell_size));
	}
	else
	{
		return sf::Vector2i(-1, -1);
	}
}

void Grid::printCells() const
{
	
	for (int i = 0; i < grid_width / cell_size; i++)
		{
			for (int j = 0; j < grid_height; j++){
				cells[j][i]->printCell();
			}
		}
		
}

void Grid::insert(Mass* particle)
{
	Mass part = *particle;
	sf::Vector2i cell_idx = getCellIndex((int)part.pos.x, (int)part.pos.y);
	//sf::Vector2i cell_idx = getCellIndex((int)particle->pos.x, (int)particle->pos.y);
	if (cell_idx.x != -1 && cell_idx.y != -1)
	{
		std::cout << "inserted on cell: " << cell_idx.x << ", " << cell_idx.y << std::endl;
		cells[cell_idx.y][cell_idx.x]->add_object(particle);
		
	}
}

void Grid::draw(sf::RenderWindow* window) const
{
	for (int i = 0; i < grid_width / cell_size; i++)
	{
		for (int j = 0; j < grid_height / cell_size; j++)
		{
			sf::RectangleShape rect(sf::Vector2f(cell_size, cell_size));
			rect.setPosition(i * cell_size, j * cell_size);
			rect.setFillColor(sf::Color::Transparent);
			rect.setOutlineColor(sf::Color::White);
			rect.setOutlineThickness(1);
			window->draw(rect);
		}
	}
}

void Grid::clearGrid()
{
	
	for (int i = 0; i < grid_width / cell_size; i++)
		{
			for (int j = 0; j < grid_height / cell_size; j++)
			{
				cells[j][i]->clear();
			}
		}
	
}

//cell

Grid::cell::cell(int x, int y)
{
	//std::cout << " cell constructor called on cell : (" <<x << ", " << y << std::endl;
	this->cell_x = x;
	this->cell_y = y;
	this->object_count = 0;

}

void Grid::cell::printCell() const
{
	//std::cout << "CELL : (" << (this->cell_x) << ", " << (this->cell_y) << ") | CONTENTS: " << (object_count) << std::endl;
}

void Grid::cell::add_object(Mass* object)
{
	std::cout << "CELL : (" << (this->cell_x) << ", " << (this->cell_y) << ") | CONTENTS: " << (object_count) << std::endl;

	if (object_count < cell_capacity)
	{
		objects[object_count] = object;
		object_count++;
	}
	else
	{
		std::cout << "Cell is full" << std::endl;
	}
}

void Grid::cell::remove_object(int object_idx)
{
}

void Grid::cell::clear()
{
	object_count = 0;
	Mass* objects[4] = {};

}
