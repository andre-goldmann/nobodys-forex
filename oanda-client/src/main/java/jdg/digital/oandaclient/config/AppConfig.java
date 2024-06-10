package jdg.digital.oandaclient.config;

import com.oanda.v20.Context;
import com.oanda.v20.ContextBuilder;
import com.oanda.v20.ExecuteException;
import com.oanda.v20.RequestException;
import com.oanda.v20.account.Account;
import com.oanda.v20.account.AccountID;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.beans.factory.annotation.Value;

@Configuration
public class AppConfig {

    @Bean
    Context oandaCtx(
            @Value("${oanda.url}") String oandaUrl,
            @Value("${oanda.api-key}") String oandaApiKey){
        return new ContextBuilder(oandaUrl)
                .setApplication("OandaClient")
                .setToken(oandaApiKey)
                .build();
    }

    @Bean
    Account accountOne(final Context oandayCtx,
                       @Value("${oanda.accOne}") String accountId) throws ExecuteException, RequestException {
        return oandayCtx.account.get(new AccountID(accountId)).getAccount();
    }

    @Bean
    Account accountTwo(final Context oandayCtx,
                       @Value("${oanda.accTwo}") String accountId) throws ExecuteException, RequestException {
        return oandayCtx.account.get(new AccountID(accountId)).getAccount();
    }

    @Bean
    Account accountThree(final Context oandayCtx,
                       @Value("${oanda.accThree}") String accountId) throws ExecuteException, RequestException {
        return oandayCtx.account.get(new AccountID(accountId)).getAccount();
    }

    @Bean
    Account accountFour(final Context oandayCtx,
                         @Value("${oanda.accFour}") String accountId) throws ExecuteException, RequestException {
        return oandayCtx.account.get(new AccountID(accountId)).getAccount();
    }

    @Bean
    Account accountFive(final Context oandayCtx,
                         @Value("${oanda.accFive}") String accountId) throws ExecuteException, RequestException {
        return oandayCtx.account.get(new AccountID(accountId)).getAccount();
    }

}
