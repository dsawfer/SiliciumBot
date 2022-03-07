package com.zhivaevartem.siliciumbot.bot.listener;

import java.util.List;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import org.springframework.stereotype.Component;

/**
 * Listen help commands. E.g. help, github...
 */
@Component
public class HelpCommandListener extends AbstractCommandListener {

  @Override
  protected void onCommandReceived(String command, List<String> args,
      MessageReceivedEvent event) {
    event.getChannel().sendMessage(command).queue();
    event.getChannel().sendMessage(String.join(";", args)).queue();
  }
}
