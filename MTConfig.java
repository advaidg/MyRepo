@Configuration
@EnableBatchProcessing
public class BatchConfiguration {

    @Autowired
    private JobBuilderFactory jobBuilderFactory;

    @Autowired
    private StepBuilderFactory stepBuilderFactory;

    @Bean
    public MultiThreadedJsonItemReader<MyObject> reader() {
        return new MultiThreadedJsonItemReader<>("path/to/file.json", MyObject.class, 1000);
    }

    @Bean
    public ItemProcessor<List<MyObject>, List<MyObject>> processor() {
        // ...
    }

    @Bean
    public ItemWriter<List<MyObject>> writer() {
        // ...
    }

    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor taskExecutor = new ThreadPoolTaskExecutor();
        taskExecutor.setCorePoolSize(4);
        taskExecutor.setMaxPoolSize(8);
        taskExecutor.setQueueCapacity(100);
        return taskExecutor;
    }

    @Bean
    public Step step() {
        return stepBuilderFactory.get("step")
                .<List<MyObject>, List<MyObject>>chunk(10)
                .reader(reader())
                .processor(processor())
                .writer(writer())
                .taskExecutor(taskExecutor())
                .build();
    }

    @Bean
    public Job job() {
        return jobBuilderFactory.get("job")
                .start(step())
                .build();
    }
}
