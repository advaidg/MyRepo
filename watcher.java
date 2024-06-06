   @Bean
    CommandLineRunner init(DirectoryWatcherService watcherService) {
        return args -> {
            new Thread(() -> watcherService.watchDirectory()).start();
        };
    }
