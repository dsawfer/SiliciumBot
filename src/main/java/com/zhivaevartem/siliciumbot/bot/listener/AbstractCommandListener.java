package com.zhivaevartem.siliciumbot.bot.listener;

import com.zhivaevartem.siliciumbot.persistence.service.BotGuildConfigService;
import com.zhivaevartem.siliciumbot.util.StringUtils;
import java.util.List;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.codehaus.plexus.util.cli.CommandLineUtils;
import org.jetbrains.annotations.NotNull;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Base event listener class handle commands.
 */
public abstract class AbstractCommandListener extends ListenerAdapter {
  private BotGuildConfigService botGuildConfigService;

  @Autowired
  public final void setBotGuildConfigService(BotGuildConfigService botGuildConfigService) {
    this.botGuildConfigService = botGuildConfigService;
  }

  @Override
  public final void onMessageReceived(
      @NotNull MessageReceivedEvent event) {
    String content = event.getMessage().getContentDisplay();
    String prefix = this.botGuildConfigService.getPrefix(event.getGuild().getId());
    if (!event.getAuthor().isBot() && content.startsWith(prefix)) {
      content = content.substring(prefix.length());
      List<String> args = StringUtils.parseArguments(content);
      if (args.size() > 0) {
        String command = args.get(0);
        args.remove(0);
        this.onCommandReceived(command, args, event);
      }
    }
  }

  protected void onCommandReceived(String command, List<String> args, MessageReceivedEvent event) {}
}
