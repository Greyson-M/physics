
#include <iostream>
#include <string>
#include <sstream>
#include "Environment.h"
#include "Mass.h"


//private methods
void Environment::initWindow()
{
	this->window = nullptr;
}


void Environment::initVariables()
{
	

	this->particle_count = 0;
	this->max_particles = sizeof(this->mass_list);
	
	this->particle_radius = 10;
	
	videoMode.height = 720;
	videoMode.width = 1280;
	width = 1280;
	height = 720;
	this->window = new sf::RenderWindow(videoMode, "SFML works!");
	this->window->setFramerateLimit(fps_target);

	this->grid = Grid(width, height);


	
}


//constructor / destructor
Environment::Environment()
{
	initWindow();
	initVariables();
	
}

Environment::~Environment()
{
	delete this->window;
}

void Environment::attract(Mass* particle)
{	

	const sf::Vector2f screen_center = sf::Vector2f((width / 2), (height / 2));
	const float attraction_constant = 0.01f;
	const float dampening_constant = 10.f;
	const sf::Vector2f displacement = screen_center - particle->pos;
	float distance = sqrt(pow(displacement.x, 2) + pow(displacement.y, 2));

	if (distance < 1.f) {
		distance = 1.f;
	}

	const sf::Vector2f dhat = sf::Vector2f(displacement.x / distance, displacement.y / distance);

	//const sf::Vector2f vel = sf::Vector2f(displacement.x * attraction_constant + (dhat.x * (dampening_constant / distance)),
	//	displacement.y * attraction_constant + (dhat.y * (dampening_constant / distance)));

	const sf::Vector2f vel = sf::Vector2f(displacement.x * attraction_constant,
		displacement.y * attraction_constant);

	particle->addVelocity(vel);
	

}

//getters
const bool Environment::running() const
{
	return this->window->isOpen();
}

void Environment::updateGrid()
{
	grid->clearGrid();
	for (int i = 0; i < particle_count; i++) {
			grid->insertObject(mass_list[i]);
		}
}

bool Environment::inBounds(int x, int y)
{
	return x > 0 && x < width && y > 1 && y < height;
}

sf::Vector2i Environment::getCellIndex(int x, int y)
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

void Environment::clearGrid()
{
	for (int i = 0; i < height / cell_size; i++) {
		for (int j = 0; j < width / cell_size; j++) {
			grid[i][j]->clear();
		}
	}
}


void Environment::insertObject(Mass* particle)
{
	sf::Vector2i cell_idx = getCellIndex(particle->pos.x, particle->pos.y);
	if (cell_idx.x != -1 && cell_idx.y != -1) {
		grid[cell_idx.x][cell_idx.y]->add_object(particle);
	}
}



bool Environment::isColliding(Mass* particle1, Mass* particle2)
{
	const sf::Vector2f displacement = particle1->pos - particle2->pos;
	const float distsq = displacement.x * displacement.x + displacement.y * displacement.y;
	const float radii = particle1->radius + particle2->radius;

	if (distsq < radii * radii) {
		return true;
	}
	else {
		return false;
	}
}

void Environment::resolveCollision(Mass* particle1, Mass* particle2)
{
	const float response_coef = 0.75f;

	const sf::Vector2f displacement = particle1->pos - particle2->pos;
	float distsq = displacement.x * displacement.x + displacement.y * displacement.y;
	const float dist = sqrt(distsq);
	
	const sf::Vector2f dhat = displacement / dist;
	const float mass_ratio1 = particle2->mass / (particle1->mass + particle2->mass);
	const float mass_ratio2 = particle1->mass / (particle1->mass + particle2->mass);

	const float delta = 0.5f * response_coef * (dist - particle1->radius - particle2->radius);

	particle1->pos -= dhat * delta * mass_ratio2;
	particle2->pos += dhat * delta * mass_ratio1;

	
} 



//functions
void Environment::update(float fps)
{
	std::stringstream ss;

	ss << "FPS: " << fps << " | Particles: " << particle_count;
	this->window->setTitle(ss.str());

	//Event Loop
	while (window->pollEvent(ev)) {
		if (ev.type == sf::Event::Closed) window->close();		//check for close event
	}


	updateGrid();
	

	//std:: cout << "Particle count: " << sizeof(mass_list)/sizeof(mass_list[0]) << std::endl;

	sf::Vector2i directions[] = {sf::Vector2i(0, 0), sf::Vector2i(1, 0), sf::Vector2i(0, 1), sf::Vector2i(-1, 0), sf::Vector2i(0, -1), sf::Vector2i(1, 1), 
									sf::Vector2i(-1, -1), sf::Vector2i(1, -1), sf::Vector2i(-1, 1)};

	for (int i = 0; i < particle_count; i++) {
		mass_list[i]->update(this->dt);
		this->attract(mass_list[i]);

		Mass* curr_mass = mass_list[i];
		sf::Vector2f curr_pos = curr_mass->pos;

		
		for (int j = 0; j < 8; j++) {
			sf::Vector2i curr_dir = directions[j];
			int dx = curr_dir.x;
			int dy = curr_dir.y;
			sf::Vector2i cell_idx = getCellIndex(curr_pos.x, curr_pos.y);
			sf::Vector2i neighbor_idx = sf::Vector2i(cell_idx.x + dx, cell_idx.y + dy);

			if (inBounds(neighbor_idx.x*cell_size, neighbor_idx.y * cell_size)) {

				//std::cout << neighbor_idx.x << " " << neighbor_idx.y << std::endl;
				//std::cout << grid.cells[neighbor_idx.y][neighbor_idx.x].object_count << std::endl;

				if (grid.cells[neighbor_idx.y][neighbor_idx.x]->object_count > 0) {
					//std::cout << i << " is Near Particle!" << std::endl;
					for (int k = 0; k < grid[neighbor_idx.y][neighbor_idx.x]->object_count; k++) {
						if (isColliding(mass_list[i], grid.cells[neighbor_idx.y][neighbor_idx.x]->objects[k])) {
							resolveCollision(mass_list[i], grid.cells[neighbor_idx.y][neighbor_idx.x]->objects[k]);
						}
					}
				}
			}
			
			
		}
		

		/*
		for (int j = 0; j < particle_count; j++) {
			if (this->isColliding(mass_list[i], mass_list[j]) && i != j) {
				this->resolveCollision(mass_list[i], mass_list[j]);
			}
		}
		*/
	}


}

void Environment::draw()
{

	window->clear(sf::Color(217, 217, 217, 255));		//clear screen

	//draw stuff here
	grid.draw(window);

	for (int i = 0; i < particle_count; i++) {
		std::cout << i << ": " << mass_list[i]->pos.x << " " << mass_list[i]->pos.y << std::endl;
		mass_list[i]->draw(window);
	}

	//update display
	window->display();
	

}


Mass* Environment::addMass(float x, float y, float mass)
{
	

	if (particle_count < max_particles) {
		Mass* new_mass = new Mass(x, y, mass, sf::Color::Black);

		this->mass_list[particle_count] = new_mass;
		this->particle_count++;
		
		return new_mass;

	}
	else {
		std::cout << "Max particles reached" << std::endl;
		return nullptr;
	}
	

}


