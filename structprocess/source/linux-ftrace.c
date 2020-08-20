#include "config.h"

struct trace_array {
	struct list_head	list;
	char			*name;
	struct trace_buffer	trace_buffer;
#ifdef CONFIG_TRACER_MAX_TRACE
	/*
	 * The max_buffer is used to snapshot the trace when a maximum
	 * latency is reached, or when the user initiates a snapshot.
	 * Some tracers will use this to store a maximum trace while
	 * it continues examining live traces.
	 *
	 * The buffers for the max_buffer are set up the same as the trace_buffer
	 * When a snapshot is taken, the buffer of the max_buffer is swapped
	 * with the buffer of the trace_buffer and the buffers are reset for
	 * the trace_buffer so the tracing can continue.
	 */
	struct trace_buffer	max_buffer;
	bool			allocated_snapshot;
#endif
#if defined(CONFIG_TRACER_MAX_TRACE) || defined(CONFIG_HWLAT_TRACER)
	unsigned long		max_latency;
#endif
	struct trace_pid_list	__rcu *filtered_pids;
	/*
	 * max_lock is used to protect the swapping of buffers
	 * when taking a max snapshot. The buffers themselves are
	 * protected by per_cpu spinlocks. But the action of the swap
	 * needs its own lock.
	 *
	 * This is defined as a arch_spinlock_t in order to help
	 * with performance when lockdep debugging is enabled.
	 *
	 * It is also used in other places outside the update_max_tr
	 * so it needs to be defined outside of the
	 * CONFIG_TRACER_MAX_TRACE.
	 */
	arch_spinlock_t		max_lock;
	int			buffer_disabled;
#ifdef CONFIG_FTRACE_SYSCALLS
	int			sys_refcount_enter;
	int			sys_refcount_exit;
	struct trace_event_file __rcu *enter_syscall_files[NR_syscalls];
	struct trace_event_file __rcu *exit_syscall_files[NR_syscalls];
#endif
	int			stop_count;
	int			clock_id;
	int			nr_topts;
	struct tracer		*current_trace;
	unsigned int		trace_flags;
	unsigned char		trace_flags_index[TRACE_FLAGS_MAX_SIZE];
	unsigned int		flags;
	raw_spinlock_t		start_lock;
	struct dentry		*dir;
	struct dentry		*options;
	struct dentry		*percpu_dir;
	struct dentry		*event_dir;
	struct trace_options	*topts;
	struct list_head	systems;
	struct list_head	events;
	cpumask_var_t		tracing_cpumask; /* only trace on set CPUs */
	int			ref;
#ifdef CONFIG_FUNCTION_TRACER
	struct ftrace_ops	*ops;
	struct trace_pid_list	__rcu *function_pids;
	/* function tracing enabled */
	int			function_enabled;
#endif
};


struct trace_buffer {
	struct trace_array		*tr;
	struct ring_buffer		*buffer;
	struct trace_array_cpu __percpu	*data;
	cycle_t				time_start;
	int				cpu;
};


struct ring_buffer {
	unsigned			flags;
	int				cpus;
	atomic_t			record_disabled;
	atomic_t			resize_disabled;
	cpumask_var_t			cpumask;

	struct lock_class_key		*reader_lock_key;

	struct mutex			mutex;

	struct ring_buffer_per_cpu	**buffers;

#ifdef CONFIG_HOTPLUG_CPU
	struct notifier_block		cpu_notify;
#endif
	u64				(*clock)(void);

	struct rb_irq_work		irq_work;
};


struct ring_buffer_per_cpu {
	int				cpu;
	atomic_t			record_disabled;
	struct ring_buffer		*buffer;
	raw_spinlock_t			reader_lock;	/* serialize readers */
	arch_spinlock_t			lock;
	struct lock_class_key		lock_key;
	unsigned long			nr_pages;
	unsigned int			current_context;
	struct list_head		*pages;
	struct buffer_page		*head_page;	/* read from head */
	struct buffer_page		*tail_page;	/* write to tail */
	struct buffer_page		*commit_page;	/* committed pages */
	struct buffer_page		*reader_page;
	unsigned long			lost_events;
	unsigned long			last_overrun;
	local_t				entries_bytes;
	local_t				entries;
	local_t				overrun;
	local_t				commit_overrun;
	local_t				dropped_events;
	local_t				committing;
	local_t				commits;
	unsigned long			read;
	unsigned long			read_bytes;
	u64				write_stamp;
	u64				read_stamp;
	/* ring buffer pages to update, > 0 to add, < 0 to remove */
	long				nr_pages_to_update;
	struct list_head		new_pages; /* new pages to add */
	struct work_struct		update_pages_work;
	struct completion		update_done;

	struct rb_irq_work		irq_work;
};

struct buffer_page {
	struct list_head list;		/* list of buffer pages */
	local_t		 write;		/* index for next write */
	unsigned	 read;		/* index for next read */
	local_t		 entries;	/* entries on this page */
	unsigned long	 real_end;	/* real end of data */
	struct buffer_data_page *page;	/* Actual data page */
};

struct buffer_data_page {
	u64		 time_stamp;	/* page time stamp */
	local_t		 commit;	/* write committed index */
	unsigned char	 data[] RB_ALIGN_DATA;	/* data of buffer page */
};

struct ring_buffer_event {
	kmemcheck_bitfield_begin(bitfield);
	u32		type_len:5, time_delta:27;
	kmemcheck_bitfield_end(bitfield);

	u32		array[];
};
