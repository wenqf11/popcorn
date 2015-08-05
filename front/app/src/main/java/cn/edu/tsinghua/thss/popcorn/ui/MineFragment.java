package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;

import cn.edu.tsinghua.thss.popcorn.AboutInfoActivity;
import cn.edu.tsinghua.thss.popcorn.ChangePasswordActivity;
import cn.edu.tsinghua.thss.popcorn.FeedBackActivity;
import cn.edu.tsinghua.thss.popcorn.R;
import cn.edu.tsinghua.thss.popcorn.UserInfoActivity;
import cn.edu.tsinghua.thss.popcorn.config.Config;


/**
 * @author wenqingfu
 * @email thssvince@163.com
 */

public class MineFragment extends Fragment {

    private View mineView;

    @ViewInject(R.id.id_tab_mine_avatar)
    private ImageView mineAvatar;

    @ViewInject(R.id.mine_name)
    private TextView myName;

    @ViewInject(R.id.mine_username)
    private TextView myUserName;

    @OnClick(R.id.mine_user_info)
    private void onShowUserInfo(View v){
        Intent intent = new Intent(getActivity(), UserInfoActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.change_password)
    private void onChangePsdClick(View v) {
        Intent intent = new Intent(getActivity(), ChangePasswordActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.feed_back)
    private void onFeedBackClick(View v) {
        Intent intent = new Intent(getActivity(), FeedBackActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.about_info)
    private void onAboutInfoClick(View v) {
        Intent intent = new Intent(getActivity(), AboutInfoActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);
    }

    @OnClick(R.id.log_out)
    private void onLogOutClick(View v){
        SharedPreferences sp = getActivity().getApplicationContext().getSharedPreferences("userInfo", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sp.edit();
        editor.putString("USERNAME", "");
        editor.putString("PASSWORD", "");
        editor.putString("ACCESS_TOKEN", "");
        editor.apply();
        getActivity().finish();
    }

    @Override
    public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
        super.onCreateView(inflater, container, savedInstanceState);

        if(mineView==null){
            mineView=inflater.inflate(R.layout.activity_tab_mine, null);
        }

        ViewGroup parent = (ViewGroup) mineView.getParent();
        if (parent != null) {
            parent.removeView(mineView);
        }
        ViewUtils.inject(this, mineView);

        return mineView;
    }

    @Override
    public void onStart(){
        super.onStart();
        getUserInfo();
    }

    private void getUserInfo(){
        Bitmap photo = getDiskBitmap(Config.AVATAR_FILE_PATH);
        if(photo!=null){
            Drawable drawable = new BitmapDrawable(this.getResources(),photo);
            mineAvatar.setImageDrawable(drawable);
        }

        RequestParams params = new RequestParams();
        params.addQueryStringParameter("username", Config.DEBUG_USERNAME);
        params.addQueryStringParameter("access_token", Config.ACCESS_TOKEN);

        HttpUtils http = new HttpUtils();
        http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);
        http.send(HttpRequest.HttpMethod.GET,
                Config.GET_USER_INFO_URL,
                params,
                new RequestCallBack<String>() {

                    @Override
                    public void onStart() {
                    }

                    @Override
                    public void onLoading(long total, long current, boolean isUploading) {
                    }

                    @Override
                    public void onSuccess(ResponseInfo<String> responseInfo) {
                        try {
                            JSONObject jsonObject = new JSONObject(responseInfo.result);
                            String status = jsonObject.getString("status");


                            if (status.equals("ok")) {
                                JSONObject userInfo = jsonObject.getJSONObject("data");
                                String name = userInfo.getString("name");
                                myName.setText(name);
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                        myUserName.setText(Config.DEBUG_USERNAME);
                    }


                    @Override
                    public void onFailure(HttpException error, String msg) {
                        Toast.makeText(getActivity().getApplicationContext(), error.getExceptionCode() + ":" + msg, Toast.LENGTH_SHORT).show();
                    }
                });
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState){
        super.onActivityCreated(savedInstanceState);
    }

    private Bitmap getDiskBitmap(String pathString)
    {
        Bitmap bitmap = null;
        try
        {
            File file = new File(pathString);
            if(file.exists())
            {
                bitmap = BitmapFactory.decodeFile(pathString);
            }
        } catch (Exception e)
        {
            // TODO: handle exception
        }
        return bitmap;
    }
}
