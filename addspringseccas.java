import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf().disable() // Disable CSRF protection as per your XML
            .authorizeRequests()
                .antMatchers("/facelets/logout**").permitAll()
                .antMatchers("/facelets/.*", "/facelets/.*", "/facelets/.*").denyAll()
                .antMatchers("/accessDenied.**").permitAll()
                .antMatchers("/**").hasRole("ROLE_USER")
                .anyRequest().authenticated()
            .and()
            // Configure further as needed (e.g., form login, logout handling)
            .formLogin().loginPage("/login").permitAll()
            .and()
            .logout().permitAll();
    }
}
