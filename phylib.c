#include "phylib.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {
    phylib_object * newStillBall = (phylib_object *) malloc (sizeof(phylib_object));
    if (newStillBall == NULL) {
        return NULL;
    }
    
    // Initialize
    newStillBall->type = PHYLIB_STILL_BALL;
    newStillBall->obj.still_ball.number = number;
    newStillBall->obj.still_ball.pos = *pos;

    return newStillBall;
}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ) {
    phylib_object * newRollingBall = (phylib_object *) malloc (sizeof(phylib_object));
    if (newRollingBall == NULL) {
        return NULL;
    }
    
    // Initialize
    newRollingBall->type = PHYLIB_ROLLING_BALL;
    newRollingBall->obj.rolling_ball.number = number;
    newRollingBall->obj.rolling_ball.pos = *pos;
    newRollingBall->obj.rolling_ball.vel = *vel;
    newRollingBall->obj.rolling_ball.acc = *acc;

    return newRollingBall;
}

phylib_object *phylib_new_hole( phylib_coord *pos ) {
    phylib_object * newHole = (phylib_object *) malloc (sizeof(phylib_object));
    if (newHole == NULL) {
        return NULL;
    }
    
    // Initialize
    newHole->type = PHYLIB_HOLE;
    newHole->obj.hole.pos = *pos;

    return newHole;
}

phylib_object *phylib_new_hcushion( double y ) {
    phylib_object * newHCushion = (phylib_object *) malloc (sizeof(phylib_object));
    if (newHCushion == NULL) {
        return NULL;
    }

    // Initialize
    newHCushion->type = PHYLIB_HCUSHION;
    newHCushion->obj.hcushion.y = y;

    return newHCushion;
}

phylib_object *phylib_new_vcushion( double x ) {
    phylib_object * newVCushion = (phylib_object *) malloc (sizeof(phylib_object));
    if (newVCushion == NULL) {
        return NULL;
    }

    // Initialize
    newVCushion->type = PHYLIB_VCUSHION;
    newVCushion->obj.vcushion.x = x;

    return newVCushion;
}

phylib_table *phylib_new_table( void ) {
    phylib_table * newTable = (phylib_table *) malloc (sizeof(phylib_table));
    if (newTable == NULL) {
        return NULL;
    }

    // Initialize
    newTable->time = 0.0;
    
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Hole 1
    phylib_coord posOne = {0.0, 0.0};
    newTable->object[4] = phylib_new_hole(&posOne);

    // Hole 2
    phylib_coord posTwo = {0.0, PHYLIB_TABLE_WIDTH};
    newTable->object[5] = phylib_new_hole(&posTwo);

    // Hole 3
    phylib_coord posThree = {0.0, PHYLIB_TABLE_LENGTH};
    newTable->object[6] = phylib_new_hole(&posThree);

    // Hole 4
    phylib_coord posFour = {PHYLIB_TABLE_WIDTH, 0.0};
    newTable->object[7] = phylib_new_hole(&posFour);

    // Hole 5
    phylib_coord posFive = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH};
    newTable->object[8] = phylib_new_hole(&posFive);

    // Hole 6
    phylib_coord posSix = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};
    newTable->object[9] = phylib_new_hole(&posSix);

    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        newTable->object[i] = NULL;
    }

    return newTable;
}

void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
    if (*src == NULL) {
        *dest = NULL;
    }
    else {
        phylib_object * newObject = (phylib_object *) malloc (sizeof(phylib_object));
        *dest = newObject;
        memcpy(*dest, *src, sizeof(phylib_object));
    }
}

phylib_table *phylib_copy_table( phylib_table *table ) {
    phylib_table * newTable = (phylib_table *) malloc (sizeof(phylib_table));
    if (newTable == NULL) {
        return NULL;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        phylib_copy_object(&newTable->object[i], &table->object[i]);
    }

    newTable->time = table->time;
    
    return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ) {
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            break;
        }
    }
}

void phylib_free_table( phylib_table *table ) {
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        free(table->object[i]);
    }

    free(table);
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
    phylib_coord result;

    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    return result;
}

double phylib_length( phylib_coord c ) {
    double result;

    result = sqrt((c.x * c.x) + (c.y * c.y));

    return result;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ) {
    double result;

    result = (a.x * b.x) + (a.y * b.y);

    return result;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
    phylib_coord distance, location;
    double result;

    // if obj1 is not valid
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }
    
    switch (obj2->type) {
        // case 1: obj2 is a still ball
        case PHYLIB_STILL_BALL:
            distance = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
            result = phylib_length(distance);
            result = result - (PHYLIB_BALL_DIAMETER);
            break;
        
        // case 1.5: obj2 is a rolling ball
        case PHYLIB_ROLLING_BALL:
            distance = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
            result = phylib_length(distance);
            result = result - (PHYLIB_BALL_DIAMETER);
            break;

        // case 2: obj2 is a hole
        case PHYLIB_HOLE:
            distance = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
            result = phylib_length(distance);
            result = result - (PHYLIB_HOLE_RADIUS);
            break;

        // case 3: obj2 is a hcushion
        case PHYLIB_HCUSHION:
            location.x = obj1->obj.rolling_ball.pos.x;
            location.y = obj2->obj.hcushion.y;
            distance = phylib_sub(obj1->obj.rolling_ball.pos, location);
            result = phylib_length(distance);
            result = fabs(result);
            result = result - (PHYLIB_BALL_RADIUS);
            break;

        // case 3.5: obj2 is a vcushion
        case PHYLIB_VCUSHION:
            location.x = obj2->obj.vcushion.x;
            location.y = obj1->obj.rolling_ball.pos.y;
            distance = phylib_sub(obj1->obj.rolling_ball.pos, location);
            result = phylib_length(distance);
            result = fabs(result);
            result = result - (PHYLIB_BALL_RADIUS);
            break;

        // case 4: obj2 is not a valid object
        default:
            result = -1.0;
    }

    return result;
}

void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
    double oldPosX, oldPosY, oldVelX, oldVelY, oldAccX, oldAccY;

    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    oldPosX = old->obj.rolling_ball.pos.x;
    oldPosY = old->obj.rolling_ball.pos.y;
    oldVelX = old->obj.rolling_ball.vel.x;
    oldVelY = old->obj.rolling_ball.vel.y;
    oldAccX = old->obj.rolling_ball.acc.x;
    oldAccY = old->obj.rolling_ball.acc.y;

    // Calculating the X position
    new->obj.rolling_ball.pos.x = oldPosX + (oldVelX * time) + (0.5 * oldAccX * (time * time));
    // Calculating the Y position
    new->obj.rolling_ball.pos.y = oldPosY + (oldVelY * time) + (0.5 * oldAccY * (time * time));

    // Calculating the X velocity
    new->obj.rolling_ball.vel.x = oldVelX + (oldAccX * time);
    // Calculating the Y velocity
    new->obj.rolling_ball.vel.y = oldVelY + (oldAccY * time);

    new->obj.rolling_ball.acc.x = oldAccX;
    new->obj.rolling_ball.acc.y = oldAccY;

    // Checking velocity signs for X
    if ((new->obj.rolling_ball.vel.x * oldVelX) < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    // Checking velocity signs for Y
    if ((new->obj.rolling_ball.vel.y * oldVelY) < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

unsigned char phylib_stopped( phylib_object *object ) {
    double speed = phylib_length(object->obj.rolling_ball.vel);

    if (speed < PHYLIB_VEL_EPSILON) {
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;

        return 1;
    }
    else {
        return 0;
    }
}

void phylib_bounce( phylib_object **a, phylib_object **b ) {
    phylib_coord r_ab, v_rel, n;
    double length, v_rel_n, speedA, speedB;

    // If b is not valid, do nothing
    if (b == NULL || (*b) == NULL) {
        return;
    }

    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y *= -1.0;
            (*a)->obj.rolling_ball.acc.y *= -1.0;
            break;

        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x *= -1.0;
            (*a)->obj.rolling_ball.acc.x *= -1.0;
            break;

        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL:
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            // No break as it should go directly to case 5
        
        case PHYLIB_ROLLING_BALL:
            // Position of a with respect to b
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            // Relative velocity of a with respect to b
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            // Normal vector
            length = phylib_length(r_ab);
            n.x = r_ab.x / length;
            n.y = r_ab.y / length;

            // Ratio of the relative velocity
            v_rel_n = phylib_dot_product(v_rel, n);

            // Update velocities
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

            (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * n.x);
            (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * n.y);

            // Compute speed
            speedA = phylib_length((*a)->obj.rolling_ball.vel);
            if (speedA > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = (((*a)->obj.rolling_ball.vel.x * -1.0) / speedA) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = (((*a)->obj.rolling_ball.vel.y * -1.0) / speedA) * PHYLIB_DRAG;
            }

            speedB = phylib_length((*b)->obj.rolling_ball.vel);
            if (speedB > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = (((*b)->obj.rolling_ball.vel.x * -1.0) / speedB) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = (((*b)->obj.rolling_ball.vel.y * -1.0) / speedB) * PHYLIB_DRAG;
            }

            break;
    }
}

unsigned char phylib_rolling( phylib_table *t ) {
    unsigned char result = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            result++;
        }
    }

    return result;
}

phylib_table *phylib_segment( phylib_table *table ) {
    unsigned char numberOfBalls = phylib_rolling(table);
    phylib_table * newTable = phylib_copy_table(table);
    int ballBouncedFlag, ballStoppedFlag;

    // Stop the simulation once there are no more rolling balls
    if (numberOfBalls == 0) {
        phylib_free_table(newTable);
        return NULL;
    }

    for (double time = PHYLIB_SIM_RATE; time < PHYLIB_MAX_TIME;  time += PHYLIB_SIM_RATE) {
        newTable->time += PHYLIB_SIM_RATE;
        ballBouncedFlag = 0;
        ballStoppedFlag = 0;

        // Roll each rolling ball
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(newTable->object[i], table->object[i], time);
            }
        }

        // Checking for collisions
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (i != j && newTable->object[j] != NULL && phylib_distance(newTable->object[i], newTable->object[j]) != -1.0 && phylib_distance(newTable->object[i], newTable->object[j]) < 0.0) {
                        ballBouncedFlag = 1;
                        phylib_bounce(&newTable->object[i], &newTable->object[j]);
                        break;
                    }
                }

                // Checking if a ball stopped
                if (newTable->object[i] != NULL && phylib_stopped(newTable->object[i]) == 1) {
                    ballStoppedFlag = 1;
                    break;
                }
            }

            if (ballBouncedFlag == 1) {
                break;
            }         
        }

        if (ballBouncedFlag == 1 || ballStoppedFlag == 1) {
            break;
        }
    }

    return newTable;
}

char *phylib_object_string( phylib_object *object ) {
    static char string[80];
    
    if (object==NULL) {
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type) {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y );
            break;

        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y );
            break;

        case PHYLIB_HOLE:
            snprintf( string, 80,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y );
            break;

        case PHYLIB_HCUSHION:
            snprintf( string, 80,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y );
            break;

        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
            break;
    }

    return string;
}
