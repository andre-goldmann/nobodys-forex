package jdg.digital.springai;

import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.Generation;
import org.springframework.ai.model.Media;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.ollama.api.OllamaModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.util.MimeTypeUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.web.bind.annotation.RequestParam;
import reactor.core.publisher.Flux;

import java.util.Map;

@RestController
public class OllamaChatController {

    private final OllamaChatModel chatModel;

    @Autowired
    public OllamaChatController(OllamaChatModel chatModel) {
        this.chatModel = chatModel;
    }

    @GetMapping("/ai/ollama/generate")
    public Map<String,String> generate(@RequestParam(value = "message", defaultValue = "Explain what do you see on this picture https://docs.spring.io/spring-ai/reference/_images/multimodal.test.png") String message) {
        return Map.of("generation", this.chatModel.call(message));
    }

    @GetMapping("/ai/ollama/generateStream")
    public Flux<ChatResponse> generateStream(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
        Prompt prompt = new Prompt(new UserMessage(message));
        return this.chatModel.stream(prompt);
    }

    @GetMapping("ai/ollama/explainimage")
    public Map<String,String> explainImage(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
        var imageResource = new ClassPathResource("/multimodal.test.png");

        var userMessage = new UserMessage("Explain what do you see on this picture?",
                new Media(MimeTypeUtils.IMAGE_PNG, imageResource));
        /*
        The image shows a bowl with two bananas inside and one banana that has been placed separately. There are also three apples,
        one of which is resting on the edge of the bowl. The bowl itself appears to be made of a natural material like wood or cork and
        has a handle on top for easy lifting. It's sitting on a surface with what looks like a gray tabletop in the background.
        There is no text visible in the image

        OllamaOptions options = OllamaOptions.builder().model(OllamaModel.LLAVA).build();
        Generation generation = this.chatModel.call(new Prompt(userMessage, options)).getResult();

         */
        /*
        Okay, so I need to explain what's in the image. The user provided a link, but when I click it, it just says "This link
        contains an image not available." Hmm, that's frustrating because without seeing the image, I can't really figure out what's there.
        Wait, maybe the image is only accessible through another platform or something? Or perhaps it's a placeholder. If the image isn't
        available, how can I help explain it? I might have to ask for more details or try to get a different link. Alternatively,
        if this was part of a larger context where the image is described elsewhere, maybe I can use that information.
        But in this case, since I can't see the image, my options are limited. I could try searching online for similar images based on the
        description given before, but without knowing what exactly was there, it's not helpful. Maybe I should suggest waiting for the image
        to load or checking if there were any errors when trying to access it. In summary, since the image isn't available,
        I can't provide a detailed explanation of its contents. I'll need more information about the image to be able to describe it properly.
        </think> The image you provided is currently unavailable due to an accessibility issue with the link.
        Without seeing the image or additional context, it's not possible to accurately describe its contents.
        If you could share more details or provide a different link, I'd be happy to help explain what might be in the image based
        on that information. In the meantime, please ensure you have the correct and accessible link to the image for further assistance
         */
        Generation generation = this.chatModel.call(new Prompt(userMessage)).getResult();

        return Map.of("generation", generation.getOutput().getText());

    }


}
