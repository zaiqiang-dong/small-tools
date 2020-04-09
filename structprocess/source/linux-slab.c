#include "config.h"
struct kmem_cache {
	struct kmem_cache_cpu __percpu *cpu_slab;
	/* Used for retriving partial slabs etc */
	unsigned long flags;
	unsigned long min_partial;
	int size;		/* The size of an object including meta data */
	int object_size;	/* The size of an object without meta data */
	int offset;		/* Free pointer offset. */
#ifdef CONFIG_SLUB_CPU_PARTIAL
	/* Number of per cpu partial objects to keep around */
	unsigned int cpu_partial;
#endif
	struct kmem_cache_order_objects oo;

	/* Allocation and freeing of slabs */
	struct kmem_cache_order_objects max;
	struct kmem_cache_order_objects min;
	gfp_t allocflags;	/* gfp flags to use on each alloc */
	int refcount;		/* Refcount for slab cache destroy */
	void (*ctor)(void *);
	int inuse;		/* Offset to metadata */
	int align;		/* Alignment */
	int reserved;		/* Reserved bytes at the end of slabs */
	int red_left_pad;	/* Left redzone padding size */
	const char *name;	/* Name (only for display!) */
	struct list_head list;	/* List of slab caches */
#ifdef CONFIG_SYSFS
	struct kobject kobj;	/* For sysfs */
	struct work_struct kobj_remove_work;
#endif
#ifdef CONFIG_MEMCG
	struct memcg_cache_params memcg_params;
	int max_attr_size; /* for propagation, maximum size of a stored attr */
#ifdef CONFIG_SYSFS
	struct kset *memcg_kset;
#endif
#endif

#ifdef CONFIG_SLAB_FREELIST_HARDENED
	unsigned long random;
#endif

#ifdef CONFIG_NUMA
	/*
	 * Defragmentation by allocating from a remote node.
	 */
	int remote_node_defrag_ratio;
#endif

#ifdef CONFIG_SLAB_FREELIST_RANDOM
	unsigned int *random_seq;
#endif

#ifdef CONFIG_KASAN
	struct kasan_cache kasan_info;
#endif

	struct kmem_cache_node *node[MAX_NUMNODES];
};


struct kmem_cache_cpu {
	void **freelist;	/* Pointer to next available object */
	unsigned long tid;	/* Globally unique transaction id */
	struct page *page;	/* The slab from which we are allocating */
#ifdef CONFIG_SLUB_CPU_PARTIAL
	struct page *partial;	/* Partially allocated frozen slabs */
#endif
	unsigned int stat[NR_SLUB_STAT_ITEMS];
};

struct kmem_cache_order_objects {
	unsigned long x;
};

struct kmem_cache_node {
	spinlock_t list_lock;

#ifdef CONFIG_SLAB
	struct list_head slabs_partial;	/* partial list first, better asm code */
	struct list_head slabs_full;
	struct list_head slabs_free;
	unsigned long total_slabs;	/* length of all slab lists */
	unsigned long free_slabs;	/* length of free slab list only */
	unsigned long free_objects;
	unsigned int free_limit;
	unsigned int colour_next;	/* Per-node cache coloring */
	struct array_cache *shared;	/* shared per node */
	struct alien_cache **alien;	/* on other nodes */
	unsigned long next_reap;	/* updated without locking */
	int free_touched;		/* updated without locking */
#endif

#ifdef CONFIG_SLUB
	unsigned long nr_partial;
	struct list_head partial;
#ifdef CONFIG_SLUB_DEBUG
	atomic_long_t nr_slabs;
	atomic_long_t total_objects;
	struct list_head full;
#endif
#endif

};
