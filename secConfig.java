
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf().disable()  // Disable CSRF protection
            .exceptionHandling()
                .authenticationEntryPoint(casProcessingFilterEntryPoint())  // Configure CAS Entry Point
                .and()
            .authorizeRequests()
                .accessDecisionManager(accessDecisionManager())  // Set custom AccessDecisionManager
                .antMatchers("/accessDenied.*").permitAll()  // Public screens
                .antMatchers("/**").hasRole("USER")  // Application screens require ROLE_USER
                .and()
            .addFilterAt(casAuthenticationFilter(), CasAuthenticationFilter.class)  // Add CAS Authentication Filter
            .sessionManagement()
                .maximumSessions(1)
                .maxSessionsPreventsLogin(true)  // Restrict to 1 session per user, prevent additional logins
                .and()
            .and()
            .logout()
                .logoutUrl("/j_spring_cas_security_logout")
                .logoutSuccessHandler(dciLogoutSuccessHandler())
                .invalidateHttpSession(true);  // Invalidate session on logout
    }
