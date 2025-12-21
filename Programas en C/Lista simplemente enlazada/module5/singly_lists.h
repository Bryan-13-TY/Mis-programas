#ifndef SINGLY_LISTS_H
#define SINGLY_LISTS_H

#include <stddef.h>
#include <stdbool.h>

typedef enum {
    LIST_OK = 0,
    LIST_ERR_NULL = -1,
    LIST_ERR_EMPTY = -2,
    LIST_ERR_ALLOC = -3,
    LIST_ERR_NOT_INSERTED = -4,
    LIST_ERR_OUT_OF_RANGE = -5,
    LIST_ERR_NOT_FOUND = -6
} ListStatus;

typedef struct SList SList;

SList *slist_create(void);
ListStatus slist_size(SList *list, int *count);
ListStatus slist_size_bytes(SList *list, size_t *bytes);
ListStatus slist_is_empty(SList *list, bool *is_empty);
ListStatus slist_push_back(SList *list, int num);
ListStatus slist_push_front(SList *list, int num);
ListStatus slist_insert_in_position(SList *list, int num, int pos);
ListStatus slist_change_value(SList *list, int num, int pos);
ListStatus slist_search_for_value(SList *list, int num, int *pos);
ListStatus slist_search_for_position(SList *list, int pos, int *value);
ListStatus slist_front(SList *list, int *value);
ListStatus slist_back(SList *list, int *value);
ListStatus slist_free_in_position(SList *list, int pos);
ListStatus slist_clear(SList *list);
ListStatus slist_sum(SList *list, int *sum);
ListStatus slist_destroy(SList *list);
void slist_show(SList *list);

#endif