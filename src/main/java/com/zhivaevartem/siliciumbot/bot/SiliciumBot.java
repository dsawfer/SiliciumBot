package com.zhivaevartem.siliciumbot.bot;

import com.zhivaevartem.siliciumbot.bot.listener.AbstractCommandListener;
import com.zhivaevartem.siliciumbot.bot.listener.HelpCommandListener;
import javax.security.auth.login.LoginException;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Discord bot bean.
 */
@Component
public class SiliciumBot {
  @Value("${siliciumbot.token}")
  private String token;

  @Autowired
  private HelpCommandListener helpCommandListener;

  private JDA jda;

  public SiliciumBot() {}

  public void start() throws LoginException {
    this.jda = JDABuilder.createDefault(this.token).build();
    this.jda.addEventListener(this.helpCommandListener);
  }
}
