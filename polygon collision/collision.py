import numpy as np
import pygame    

class Collision:
    def __init__(self, env):
        self.env = env
        self.WIN = env.WIN
        self.gons = env.gons
        self.font = env.font

    def collision_check(self, p1, p2):
        min_overlap = float('inf')
        collision_axis = None

        for polygon in [p1, p2]:
            for i in range(len(polygon.points)):
                # Get the current point and the next point in the polygon
                point1 = polygon.points[i]
                point2 = polygon.points[(i + 1) % len(polygon.points)]

                # Compute the edge vector
                edge = point2 - point1

                # Compute the axis perpendicular to the edge
                axis = np.array([-edge[1], edge[0]])
                axis /= np.linalg.norm(axis)

                # Project both polygons onto the axis
                projection1 = np.dot(p1.points, axis)
                projection2 = np.dot(p2.points, axis)

                # Compute the overlap between the projections
                overlap = min(projection1.max(), projection2.max()) - max(projection1.min(), projection2.min())
                if overlap < 0:
                    # The projections do not overlap, so the polygons do not overlap
                    return None
                elif overlap < min_overlap:
                    # This is the smallest overlap so far, so store it and the corresponding axis
                    min_overlap = overlap
                    collision_axis = axis

        # The projections overlap on all axes, so the polygons overlap
        # Return the smallest overlap and the corresponding axis
        return min_overlap, collision_axis
    
    # Checking if a point is inside a polygon
    def point_in_polygon(self, point, polygon):
        num_vertices = len(polygon)
        x, y = point[0], point[1]
        inside = False
    
        # Store the first point in the polygon and initialize the second point
        p1 = polygon[0]
    
        # Loop through each edge in the polygon
        for i in range(1, num_vertices + 1):
            # Get the next point in the polygon
            p2 = polygon[i % num_vertices]
    
            # Check if the point is above the minimum y coordinate of the edge
            if y > min(p1[1], p2[1]):
                # Check if the point is below the maximum y coordinate of the edge
                if y <= max(p1[1], p2[1]):
                    # Check if the point is to the left of the maximum x coordinate of the edge
                    if x <= max(p1[0], p2[0]):
                        # Calculate the x-intersection of the line connecting the point to the edge
                        x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[1]
    
                        # Check if the point is on the same line as the edge or to the left of the x-intersection
                        if p1[0] == p2[0] or x <= x_intersection:
                            # Flip the inside flag
                            inside = not inside
    
            # Store the current point as the first point for the next iteration
            p1 = p2
    
        # Return the value of the inside flag
        return inside
    
    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        # Check if the intersection point is within the bounds of both line segments
        if min(line1[0][0], line1[1][0]) <= x <= max(line1[0][0], line1[1][0]) and min(line1[0][1], line1[1][1]) <= y <= max(line1[0][1], line1[1][1]) and min(line2[0][0], line2[1][0]) <= x <= max(line2[0][0], line2[1][0]) and min(line2[0][1], line2[1][1]) <= y <= max(line2[0][1], line2[1][1]):
            return x, y
        else:
            return None

    def find_collision_points(self, p1, p2):
        collision_points = []
        for i in range(len(p1.points)):
            for j in range(len(p2.points)):
                point1 = p1.points[i]
                point2 = p1.points[(i + 1) % len(p1.points)]
                point3 = p2.points[j]
                point4 = p2.points[(j + 1) % len(p2.points)]
                intersection = self.line_intersection((point1, point2), (point3, point4))
                if intersection:
                    collision_points.append(intersection)
        return collision_points
    
    # def collision_response(self, overlap, axis, p1, p2, cp):
    #     response_coefficient = 0.5
    #     # Compute the center of the polygons
    #     center1 = np.mean(p1.points, axis=0)
    #     center2 = np.mean(p2.points, axis=0)

    #     # Compute the collision normal
    #     # collision_normal = center1 - center2
    #     # collision_normal = collision_normal / np.linalg.norm(collision_normal)
    #     collision_normal = axis/ np.linalg.norm(axis)
        
    #     # Ensure the collision normal points from p1 to p2
    #     if np.dot(collision_normal, center2 - center1) < 0:
    #         collision_normal = -collision_normal

    #     # Compute the relative velocity of the two polygons at the point of collision
    #     r1 = cp - center1
    #     r2 = cp - center2

    #     #print ("R1 ", r1)
    #     #print ("R2 ", r2)

    #     r1_perp = np.array([-r1[1], r1[0]])
    #     r2_perp = np.array([-r2[1], r2[0]])
    #     rdotn1 = np.dot(r1_perp, collision_normal)
    #     rdotn2 = np.dot(r2_perp, collision_normal)

    #     relative_velocity = p1.vel + p1.angle_vel * r1_perp - p2.vel - p2.angle_vel * r2_perp

    #     contact_velocity = np.dot(relative_velocity, collision_normal)
    #     if contact_velocity > 0:
    #         print ("Contact Velocity: ", contact_velocity)
    #         return

    #     inertia1 = (1/12) * p1.mass * (4 * (30*30) + (30*30))
    #     inertia2 = (1/12) * p2.mass * (4 * (30*30) + (30*30))

    #     impulse_scalar = -(1 + response_coefficient) * contact_velocity / ((1/p1.mass + 1/p2.mass) + (rdotn1*rdotn1/inertia1) + (rdotn2*rdotn2/inertia2))
    #     impulse = impulse_scalar * collision_normal
    #     print(impulse)

    #     return impulse



    # def collision_response(self, p1, p2, collision_point):
    #     response_coefficient = 0.5

    #     # Compute the center of the polygons
    #     center1 = np.mean(p1.points, axis=0)
    #     center2 = np.mean(p2.points, axis=0)

    #     # Compute the collision normal
    #     collision_normal = center1 - center2
    #     collision_normal = collision_normal / np.linalg.norm(collision_normal)

    #     # Compute the relative velocity of the two polygons at the point of collision
    #     r1 = collision_point - center1
    #     r2 = collision_point - center2

    #     r1_perp = np.array([-r1[1], r1[0]])
    #     r2_perp = np.array([-r2[1], r2[0]])
    #     rdotn1 = np.dot(r1_perp, collision_normal)
    #     rdotn2 = np.dot(r2_perp, collision_normal)

        
    #     relative_velocity = p1.vel + p1.angle_vel * r1_perp - p2.vel - p2.angle_vel * r2_perp

    #     contact_velocity = np.dot(relative_velocity, collision_normal)
    #     if contact_velocity > 0:
    #         return


    #     inertia1 = np.linalg.norm(r1)**2 * p1.mass
    #     inertia2 = np.linalg.norm(r2)**2 * p2.mass

    #     # Compute the impulse scalar
    #     #impulse_scalar = -(1 + response_coefficient) * contact_velocity / (1/p1.mass + 1/p2.mass + np.dot(np.cross(r1_perp, collision_normal)**2/inertia1, np.cross(r2_perp, collision_normal)**2/inertia2))
    #     impulse_scalar = -(1 + response_coefficient) * contact_velocity / ((1/p1.mass + 1/p2.mass) + (rdotn1*rdotn1/inertia1) + (rdotn2*rdotn2/inertia2))

    #     # Apply the impulse to the polygons
    #     impulse = impulse_scalar * collision_normal
    #     p1.vel += impulse / p1.mass
    #     p2.vel -= impulse / p2.mass
    #     p1.angle_vel += np.dot(r1, impulse) / inertia1
    #     p2.angle_vel -= np.dot(r2, impulse) / inertia2

    #     print (p1.vel, p2.vel, p1.angle_vel, p2.angle_vel)

    def resolve_collision(self, p1, p2, overlap, axis, contact_points):
        restitution = 0.5
        slop = 0.01  # Allowable penetration
        percent = 0.2  # Percentage of overlap to resolve per frame

        # Compute the center of the polygons
        center1 = np.mean(p1.points, axis=0)
        center2 = np.mean(p2.points, axis=0)

        # Compute the collision normal
        collision_normal = axis / np.linalg.norm(axis)

        impulse_list = []
        r1_list = []
        r2_list = []

        for point in contact_points:
            r1 = point - center1
            r2 = point - center2

            r1_list.append(r1)
            r2_list.append(r2)

            r1_perp = np.array([-r1[1], r1[0]])
            r2_perp = np.array([-r2[1], r2[0]])

            relative_velocity = p1.vel + p1.angle_vel * r1_perp - p2.vel - p2.angle_vel * r2_perp
            contact_velocity = np.dot(relative_velocity, collision_normal)
            if contact_velocity > 0:
                continue
            
            rdotn1 = np.dot(r1_perp, collision_normal)
            rdotn2 = np.dot(r2_perp, collision_normal)

            inertia1 = (1/12) * p1.mass * (4 * (30*30) + (30*30))
            inertia2 = (1/12) * p2.mass * (4 * (30*30) + (30*30))

            impulse_scalar = -(1 + restitution) * contact_velocity / ((1/p1.mass + 1/p2.mass) + (rdotn1*rdotn1/inertia1) + (rdotn2*rdotn2/inertia2))
            impulse_scalar /= len(contact_points)
            impulse = impulse_scalar * collision_normal
            impulse_list.append(impulse)

        for i, impulse in enumerate(impulse_list):
            p1.vel = np.add(p1.vel, impulse / p1.mass)
            p2.vel = np.subtract(p2.vel, impulse / p2.mass)
            p1.angle_vel += np.dot(r1_list[i], impulse) / inertia1
            p2.angle_vel -= np.dot(r2_list[i], impulse) / inertia2

        # Compute correction to resolve overlap
        correction = max(overlap - slop, 0) / (1/p1.mass + 1/p2.mass) * percent * collision_normal
        p1.points -= correction / p1.mass
        p2.points += correction / p2.mass

    def collision_update(self, gon):
        for other_gon in self.gons:
            if gon != other_gon:
                C = self.collision_check(gon, other_gon)
                if C:
                    overlap, axis = C
                    if axis is not None:
                        #print (overlap, axis)

                        c_points = self.find_collision_points(gon, other_gon)
                        print ("Collision Points: ", c_points)

                        for cp in c_points:
                            #draw a circle at the collision point
                            #print ("Collision Point: ", cp)
                            pygame.draw.circle(self.WIN, (255, 0, 0), (int(cp[0]), int(cp[1])), 5)

                        #print ("collision points: ", c_points)
                        
                        self.resolve_collision(gon, other_gon, overlap, axis, c_points)

                        # total_impulse = np.array([0, 0])
                        # remove = []
                        # print ("-"*20)
                        # for cp in c_points:
                        #     #draw a circle at the collision point
                        #     print ("Collision Point: ", cp)
                        #     pygame.draw.circle(self.WIN, (255, 0, 0), (int(cp[0]), int(cp[1])), 5)
                        #     #position test
                        #     pos_text = self.font.render(f"{cp}", True, (0, 0, 0))
                        #     self.WIN.blit(pos_text, (round(cp[0]), round(cp[1])))
                        #     pygame.display.update()
                        #     impulse = self.collision_response(overlap, axis, gon, other_gon, cp)
                        #     if impulse is None:
                        #         print ("No impulse: ", impulse)
                        #         remove.append(cp)
                        #     else:
                        #         print ("Impulse: ", impulse)
                        #         total_impulse = np.add(total_impulse, impulse)

                        # print ("remove: ", remove)
                        # for r in remove:
                        #     print ("impulse: ", total_impulse)
                        #     print ("Removing: ", r)
                        #     print ("Collision Points: ", c_points)
                        #     input()
                        #     c_points = np.delete(c_points, np.where(c_points == r), axis=0)

                        # print ("-"*20)
                            
                                    
                        # dampening = 0.5

                        # if len(c_points) > 0:
                        #     avg_impulse = total_impulse / len(c_points)
                        #     r_avg1 = np.mean([cp - np.mean(gon.points, axis=0) for cp in c_points], axis=0)
                        #     r_avg2 = np.mean([cp - np.mean(other_gon.points, axis=0) for cp in c_points], axis=0)
                            # inertia1 = np.linalg.norm(r_avg1)**2 * gon.mass
                            # inertia2 = np.linalg.norm(r_avg2)**2 * other_gon.mass

                            # inertia1 = (1/12) * gon.mass * (4 * (30*30) + (30*30))
                            # inertia2 = (1/12) * other_gon.mass * (4 * (30*30) + (30*30))
                            
                            # if np.linalg.norm(r_avg1) < 1:

                            #     pass
                            #     print ("-------------------")
                            #     print ("Center 1: ", np.mean(gon.points, axis=0))
                            #     print ("Collision Points: ", c_points)
                            #     print ("R1: ", r_avg1, "R2: ", np.linalg.norm(r_avg2))
                            #     print ("Impulse: ", avg_impulse)
                            #     print ("Impulses: ", total_impulse)
                                        

                                    #print ("R1: ", np.linalg.norm(r_avg1), "R2: ", np.linalg.norm(r_avg2))

                            # gon.vel = np.add(gon.vel, avg_impulse / gon.mass)
                            # other_gon.vel = np.subtract(other_gon.vel, avg_impulse / other_gon.mass)
                            # gon.angle_vel = np.add(gon.angle_vel, dampening * -(avg_impulse[0] * r_avg1[1] - avg_impulse[1] * r_avg1[0]) / inertia1) 
                            # other_gon.angle_vel = np.subtract(other_gon.angle_vel, dampening * -(avg_impulse[0] * r_avg2[1] - avg_impulse[1] * r_avg2[0]) / inertia2)

                        # delta = axis * overlap/2
                        # gon.points += delta
                        # other_gon.points -= delta
                        
                        # gon.move((delta * axis[0])/2, (delta * axis[1])/2)
                        # other_gon.move((-delta * axis[0])/2, (-delta * axis[1])/2)                   
                
                # collision_point = self.collision_check(gon, other_gon)
                # if collision_point:
                #     self.collision_response(gon, other_gon, collision_point)
