import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.cas.ServiceProperties;
import org.springframework.security.cas.web.CasAuthenticationFilter;
import org.springframework.security.cas.web.CasAuthenticationEntryPoint;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
            .antMatchers("/secure/**").authenticated()
            .anyRequest().permitAll()
            .and()
            .addFilterBefore(casAuthenticationFilter(), BasicAuthenticationFilter.class)
            .exceptionHandling()
            .authenticationEntryPoint(casAuthenticationEntryPoint());
    }

    // CAS Authentication EntryPoint setup
    public CasAuthenticationEntryPoint casAuthenticationEntryPoint() {
        CasAuthenticationEntryPoint entryPoint = new CasAuthenticationEntryPoint();
        entryPoint.setLoginUrl("https://your-cas-url/login");
        entryPoint.setServiceProperties(serviceProperties());
        return entryPoint;
    }

    // CAS Service Properties
    public ServiceProperties serviceProperties() {
        ServiceProperties serviceProperties = new ServiceProperties();
        serviceProperties.setService("http://your-app-url/login/cas");
        serviceProperties.setSendRenew(false);
        return serviceProperties;
    }

    // CAS Authentication Filter
    public CasAuthenticationFilter casAuthenticationFilter() throws Exception {
        CasAuthenticationFilter filter = new CasAuthenticationFilter();
        filter.setAuthenticationManager(authenticationManager());
        filter.setServiceProperties(serviceProperties());
        return filter;
    }
}
